from flask import Flask, request, abort
import os
from dotenv import load_dotenv
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SIGNAL_INVITE_LINK = os.getenv('SIGNAL_INVITE_LINK')
OPEN_PORT = os.getenv('OPEN_PORT', 5000)  # Default to 5000 if OPEN_PORT not set
REPO_NAME = os.getenv('REPO_NAME')
@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        data = request.json
        try:
            pr_number = data['pull_request']['number']
            REPO_NAME = data['repository']['full_name']
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

def post_signal_invite(REPO_NAME, pr_number):
    comment_url = f"https://api.github.com/repos/{REPO_NAME}/issues/{pr_number}/comments"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    comment = {'body': f'Thank you for your pull request! Join our Signal chat here: {SIGNAL_INVITE_LINK}'}
    try:
        response = requests.post(comment_url, json=comment, headers=headers)
        if response.status_code == 201:
            logging.info(f'Comment posted successfully on PR #{pr_number} in {REPO_NAME}')
            return 'Comment posted successfully', 200
        else:
            logging.error(f'Failed to post comment: {response.status_code} {response.text}')
            return 'Failed to post comment', 500
    except requests.RequestException as e:
        logging.error(f"Failed to connect to GitHub: {e}")
        return 'Failed to connect to GitHub', 500

if __name__ == '__main__':
    app.run(debug=True, port=int(OPEN_PORT))