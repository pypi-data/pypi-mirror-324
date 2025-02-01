import boto3
import json
import base64
import requests
import logging
import time
from Crypto.Cipher import AES
from datetime import datetime, timedelta
import uuid
import mysql.connector  # Import mysql.connector for database operations

# Constants
MAX_RETRIES = 3
RETRY_DELAY = 2

def get_secret(secret_name):
    # Fetch the secret from AWS Secrets Manager
    client = boto3.client('secretsmanager', region_name='us-west-2')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def decrypt_oauth_credentials(store):
    # Fetch the encryption keys
    encryption_keys = get_secret("prod/walmart-oauth-encryption-keys")

    # Decode the key and IV from hex
    key = bytes.fromhex(encryption_keys["ENCRYPTION_KEY"])
    iv = bytes.fromhex(encryption_keys["ENCRYPTION_IV"])

    # Decrypt function
    def decrypt_field(encrypted_hex_str):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(bytes.fromhex(encrypted_hex_str))
        pad_len = decrypted_data[-1]
        return decrypted_data[:-pad_len].decode('utf-8')

    decrypted_credentials = {}
    for field in ['access_token', 'refresh_token']:
        if field in store:
            decrypted_credentials[field] = decrypt_field(store[field])

    return decrypted_credentials

def encrypt_field(plain_text_str, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # PKCS7 padding
    pad_len = 16 - (len(plain_text_str) % 16)
    padded_plain_text = plain_text_str + chr(pad_len) * pad_len
    encrypted_data = cipher.encrypt(padded_plain_text.encode('utf-8'))
    return encrypted_data.hex()

def refresh_walmart_token(credentials, wm_partner_id):
    wm_qos_correlation_id = str(uuid.uuid4())  # Generates a unique GUID for each API call
    secret_name = 'walmart-oauth-app-credentials'
    oauth_provider_credentials = get_secret(secret_name)
    client_id = oauth_provider_credentials['CLIENT_ID']
    client_secret = oauth_provider_credentials['CLIENT_SECRET']
    refresh_token = credentials['refresh_token']
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode('utf-8')).decode('utf-8')
    authorization_header = f"Basic {auth_header}"

    url = 'https://marketplace.walmartapis.com/v3/token'

    headers = {
        'WM_PARTNER.ID': wm_partner_id,
        'Authorization': authorization_header,
        'Content-Type': 'application/x-www-form-urlencoded',
        'WM_QOS.CORRELATION_ID': wm_qos_correlation_id,
        'WM_SVC.NAME': 'Walmart Marketplace',
        'Accept': 'application/json'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    retries = 0
    while retries < MAX_RETRIES:
        try:
            auth_response = requests.post(url, headers=headers, data=data)
            auth_response.raise_for_status()
            token_data = auth_response.json()
            access_token = token_data.get('access_token')
            expires_in = token_data.get('expires_in')

            if access_token:
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'expires_in': expires_in
                }
            else:
                raise ValueError("Missing tokens in response")
        except requests.exceptions.RequestException as e:
            retries += 1
            status_code = auth_response.status_code
            response_text = auth_response.text
            logging.error(f"Failed to refresh token for {wm_partner_id} (attempt {retries}/{MAX_RETRIES}): {e}")
            logging.error(f"Status Code: {status_code}, Response Text: {response_text}")
            if retries >= MAX_RETRIES:
                message = f"Failed to refresh token for company {wm_partner_id} after {MAX_RETRIES} attempts: {e}"
                send_sns_notification(message)
                return None
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logging.error(f"Unexpected error when refreshing token: {e}")
            message = f"Unexpected error when refreshing token for company {wm_partner_id}: {e}"
            send_sns_notification(message)
            return None

    logging.error(f"Access token is None for {wm_partner_id}")
    message = f"Access token is None for company {wm_partner_id}"
    send_sns_notification(message)
    return None

# Create a new database connection
def create_db_connection(secrets):
    try:
        # Database configuration
        endpoint = "thinkbig.ch6y4ms4czto.us-west-2.rds.amazonaws.com"
        dbname = "thinkbigdata"
        if endpoint == 'localhost':
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='ijfiej43243kfjds',
                database=dbname
            )
        else:
            connection = mysql.connector.connect(
                host=endpoint,
                user=secrets['username'],
                password=secrets['password'],
                database=dbname
            )
        return connection
    except Exception as e:
        logging.error(f"Failed to create a MySQL connection: {e}")
        send_sns_notification(f"Failed to create a MySQL connection: {e}")
        raise

def get_token(store):
    # Decrypt the credentials
    credentials = decrypt_oauth_credentials(store)
    wm_partner_id = store['company_id']
    token_expiration = store.get('expires_at', None)
    # Check if token will expire in the next 5 minutes
    if datetime.utcnow() > token_expiration - timedelta(minutes=5):
        # Refresh the token
        refreshed_tokens = refresh_walmart_token(credentials, wm_partner_id)
        if refreshed_tokens:
            # Fetch the encryption keys
            encryption_keys = get_secret("prod/walmart-oauth-encryption-keys")
            key = bytes.fromhex(encryption_keys["ENCRYPTION_KEY"])
            iv = bytes.fromhex(encryption_keys["ENCRYPTION_IV"])

            # Encrypt the new tokens
            store['access_token'] = encrypt_field(refreshed_tokens['access_token'], key, iv)
            store['refresh_token'] = encrypt_field(refreshed_tokens['refresh_token'], key, iv)
            store['expires_at'] = datetime.utcnow() + timedelta(seconds=int(refreshed_tokens['expires_in']))

            # Save the updated store to the database
            try:
                # Fetch database secrets
                db_secrets = get_secret('rds!db-8f49427b-4c0a-40bd-9e76-83b97d2310bd')
                # Create database connection
                connection = create_db_connection(db_secrets)
                cursor = connection.cursor()
                # Update the oauth_credentials table
                update_query = """
                    UPDATE oauth_credentials
                    SET access_token = %s, refresh_token = %s, expires_at = %s, updated_at = NOW()
                    WHERE company_id = %s
                """

                # Convert datetime object to string acceptable by MySQL
                expires_at_str = store['expires_at'].strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute(update_query, (
                    store['access_token'],
                    store['refresh_token'],
                    expires_at_str,
                    wm_partner_id
                ))

                # Commit the transaction
                connection.commit()

            except Exception as e:
                logging.error(f"Error updating tokens in database: {e}")
                send_sns_notification(f"Error updating tokens in database for company {wm_partner_id}: {e}")
                return None  # Return None if database update fails
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

            return refreshed_tokens['access_token']
        else:
            # Handle the error
            logging.error("Failed to refresh token")
            return None
    else:
        # Token is still valid
        return credentials['access_token']

# Placeholder for send_sns_notification function
def send_sns_notification(message):
    # Implement your SNS notification logic here
    print(f"SNS Notification: {message}")

# Example usage
# store = {
#     'company_id': 'your_company_id',
#     'access_token': '<encrypted_access_token>',
#     'refresh_token': '<encrypted_refresh_token>',
#     'expires_at': datetime.utcnow() - timedelta(seconds=1)  # Token expired
# }
# access_token = get_token(store)
# print(f"Access Token: {access_token}")
