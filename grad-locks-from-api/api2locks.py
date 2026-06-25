import hashlib
import io
import os
import requests
import sys
import time
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# ==================== ASSIGN LOGINS HERE ====================
# Set these in a .env file in this directory (never commit that file)
CLIENT_ID     = os.getenv("TTLOCK_CLIENT_ID",     "YOUR_CLIENT_ID")     # From Developer Panel
CLIENT_SECRET = os.getenv("TTLOCK_CLIENT_SECRET", "YOUR_CLIENT_SECRET") # From Developer Panel
USERNAME      = os.getenv("TTLOCK_USERNAME",       "YOUR_USERNAME")     # Your TTLock Phone App Login (Email or Phone)
PASSWORD      = os.getenv("TTLOCK_PASSWORD",       "YOUR_PASSWORD")     # Your TTLock Phone App Password
# ============================================================

# 1. Generate lowercase 32-character MD5 hex string required by server
password_md5 = hashlib.md5(PASSWORD.encode('utf-8')).hexdigest().lower()

# 2. Modern Consolidated Global API Domain
BASE_URL = "https://api.ttlock.com"
TOKEN_URL = f"{BASE_URL}/oauth2/token"
KEY_LIST_URL = f"{BASE_URL}/v3/key/list"

print("Requesting Account API Token from TTLock Platform...")

token_payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "password",
    "username": USERNAME,
    "password": password_md5
}

# Payload must be explicitly passed as form-urlencoded content data
headers = {"Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(TOKEN_URL, data=token_payload, headers=headers)

try:
    token_response = response.json()
except Exception:
    print("ERROR: Critical System Error: Server refused request formatting!")
    print(f"Server Routing Status Code: {response.status_code}")
    print(f"Debug Server String:\n{response.text[:300]}")
    exit()

access_token = token_response.get("access_token")
if not access_token:
    print("ERROR: Failed to Authenticate with Server!")
    print(f"Error Code Message: {token_response}")
    exit()

print("Authentication passed! Access token generated.")
print("Reading active lock profiles from your app catalog...\n")

# 3. Pull Key List detailing low-level data structures
current_timestamp_ms = int(time.time() * 1000)

key_payload = {
    "clientId": CLIENT_ID,
    "accessToken": access_token,
    "pageNo": 1,
    "pageSize": 100,
    "date": current_timestamp_ms,
    "sdkVersion": 2  # Crucial flag to return raw unencrypted keyData parameter
}

key_raw_response = requests.post(KEY_LIST_URL, data=key_payload, headers=headers)

try:
    key_response = key_raw_response.json()
except Exception:
    print("ERROR: Error parsing the returned data matrix!")
    print(f"Data Connection Status: {key_raw_response.status_code}")
    exit()

keys = key_response.get("list", [])
if not keys:
    print("WARNING: Success, but no device pairings are associated with this token.")
    print(f"Cloud Server Return Block: {key_response}")
    exit()

for item in keys:
    print(f"=== Hardware Found: {item.get('lockName')} ===")
    print(f"MAC Address          : {item.get('lockMac')}")
    print(f"Lock ID (lock_id)    : {item.get('lockId')}")

    # Check all key variable configurations used on regional systems
    aes_key = item.get('lockKey') or item.get('keyData') or item.get('keyMac')

    print(f"AES Key (lock_key)   : {aes_key}")
    print("=" * 45 + "\n")
