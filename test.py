import os
import hmac
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the GitHub secret from the environment
GITHUB_SECRET = os.getenv('GITHUB_SECRET')

if not GITHUB_SECRET:
    raise ValueError("GITHUB_SECRET environment variable not set")

# Define the payload for testing
payload = b'{"pull_request": {"number": 123}, "repository": {"full_name": "irregularchat/Full-Stack-Chat"}}'

# Generate the HMAC SHA-256 signature
mac = hmac.new(GITHUB_SECRET.encode(), msg=payload, digestmod=hashlib.sha256)
signature = f"sha256={mac.hexdigest()}"

# Print the signature
print(signature)