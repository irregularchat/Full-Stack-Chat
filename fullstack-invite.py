from flask import Flask, request, abort
import os
from dotenv import load_dotenv
import requests
import logging
import hmac
import hashlib

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Environment variables
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_SECRET = os.getenv('GITHUB_SECRET')  # Ensure this is set in your .env file
SIGNAL_INVITE_LINK = os.getenv('SIGNAL_INVITE_LINK')
OPEN_PORT = os.getenv('OPEN_PORT', 5000)  # Default to 5000 if OPEN_PORT not set
REPO_NAME = os.getenv('REPO_NAME')

# Validate environment variables
if not all([GITHUB_TOKEN, GITHUB_SECRET, SIGNAL_INVITE_LINK, REPO_NAME, OPEN_PORT]):
    logging.error("Missing required environment variables")
    exit(1)

@app.route('/')
def home():
    return "Welcome to Full Stack Invite!"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if not verify_github_signature(request):
        abort(401, 'Signature verification failed')

    if request.method == 'POST':
        data = request.json
        try:
            pr_number = data['pull_request']['number']
            logging.info(f"Received PR #{pr_number} for repository {REPO_NAME}")
            return post_signal_invite(REPO_NAME, pr_number)
        except KeyError as e:
            logging.error(f"KeyError: Missing key in data - {e}")
            abort(400, 'Invalid data received')
        except TypeError as e:
            logging.error(f"TypeError: Wrong data type encountered - {e}")
            abort(400, 'Invalid data received')
        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            abort(500, 'Internal server error')
    else:
        abort(405, 'Method not allowed')

def post_signal_invite(repo_name, pr_number):
    comment_url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    comment = {'body': f'Join the IrregularChat Full Stack Signal chat here: {SIGNAL_INVITE_LINK}'}
    
    logging.info(f"Posting comment to URL: {comment_url}")
    try:
        response = requests.post(comment_url, json=comment, headers=headers)
        if response.status_code == 201:
            logging.info(f'Comment posted successfully on PR #{pr_number} in {repo_name}')
            return 'Comment posted successfully', 200
        else:
            logging.error(f'Failed to post comment: {response.status_code} {response.text}')
            return 'Failed to post comment', 500
    except requests.RequestException as e:
        logging.error(f"Failed to connect to GitHub: {e}")
        return 'Failed to connect to GitHub', 500

def verify_github_signature(request):
    # Verify the request signature using HMAC and the GITHUB_SECRET
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        logging.error("No X-Hub-Signature-256 found in headers")
        return False

    sha_name, signature = signature.split('=')
    if sha_name != 'sha256':
        logging.error("Signature is not sha256")
        return False

    mac = hmac.new(GITHUB_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        logging.error("Signature verification failed")
        return False

    return True

if __name__ == '__main__':
    app.run(debug=True, port=int(OPEN_PORT))