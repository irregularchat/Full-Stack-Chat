import os
import hmac
import hashlib
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the GitHub secret and repo name from the environment
GITHUB_SECRET = os.getenv('GITHUB_SECRET')
REPO_NAME = os.getenv('REPO_NAME')

if not GITHUB_SECRET:
    raise ValueError("GITHUB_SECRET environment variable not set")
if not REPO_NAME:
    raise ValueError("REPO_NAME environment variable not set")

# Define the payload for testing, using the REPO_NAME from the environment
payload = f'{{"pull_request": {{"number": 123}}, "repository": {{"full_name": "{REPO_NAME}"}}}}'.encode('utf-8')

# Generate the HMAC SHA-256 signature
mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
signature = f"sha256={mac.hexdigest()}"

# Print the signature
print("Generated signature:", signature)

# Define the URL for the webhook
webhook_url = "https://fullstackinvite.irregularchat.com/webhook"

# Set the headers including the generated signature
headers = {
    "Content-Type": "application/json",
    "X-Hub-Signature-256": signature
}

# Send the POST request
response = requests.post(webhook_url, headers=headers, data=payload, verify=False)  # Set verify=False to bypass SSL verification for testing

# Print the response status and body
print("Response status:", response.status_code)
print("Response body:", response.text)