import urllib.parse
from google.auth.transport import requests
import google.auth.crypt
import google.auth.jwt
import json

save_link = {
    "iss": "<service_account_email>",
    "aud": "google",
    "typ": "savetowallet",
    "payload": {
        "offerObjects": [
            {
                "id": "your-namespace.your-object-id"
            }
        ]
    }
}

# Encode the JWT

signer = google.auth.crypt.RSASigner.from_service_account_info(
    json.load(open(SERVICE_ACCOUNT_FILE))
)

token = google.auth.jwt.encode(signer, save_link)

# Create the URL
save_url = f"https://pay.google.com/gp/v/save/{token}"
print("Save to Google Wallet URL:", save_url)
