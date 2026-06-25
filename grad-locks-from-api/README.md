# TTLock API Secrets Extractor

This script extracts lock secrets from the TTLock management API.

## Steps

1. Update the credentials to match yours:

      ```bash
      CLIENT_ID = "YOUR_CLIENT_ID"         # From Developer Panel
      CLIENT_SECRET = "YOUR_CLIENT_SECRET" # From Developer Panel
      USERNAME = "YOUR_USERNAME"           # Your TTLock Phone App Login (Email or Phone)
      PASSWORD = "YOUR_PASSWORD"           # Your TTLock Phone App Password
      ```

2. Run the script:

   ```bash
   python3 ./api2locks.py
   ```

## Output

```bash
   === Hardware Found: XXNNN_ffeedd ===
   MAC Address          : AA:BB:CC:DD:EE:FF
   Lock ID (lock_id)    : 12345678
   AES Key (lock_key)   : AES_KEY_44_CHARACTERS
   =============================================
```

This data can be used in the ESPHome configuration e.g.: in secrets.yaml

```yaml
# TTLock Secret Cryptographic Keys
fd_address: "AA:BB:CC:DD:EE:FF"  # Replace with your lock's MAC Address
fd_aes_key: "AES_KEY_44_CHARACTERS"  # Replace with your actual AES key
```
