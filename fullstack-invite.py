#fullstack-invite.py
from flask import Flask, request, abort
import os
from dotenv import load_dotenv
import requests

app = Flask(__name__)
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
SIGNAL_INVITE_LINK = os.getenv('SIGNAL_INVITE_LINK')

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if request.method == 'POST':
        data = request.json
        try:
            pr_number = data['pull_request']['number']
            repo_name = data['repository']['full_name']
            return post_signal_invite(repo_name, pr_number)
        except (KeyError, TypeError):
            abort(400, 'Invalid data received')
    else:
        abort(405, 'Method not allowed')

def post_signal_invite(repo_name, pr_number):
    comment_url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    comment = {'body': f'Thank you for your pull request! Join our Signal chat here: {SIGNAL_INVITE_LINK}'}
    response = requests.post(comment_url, json=comment, headers=headers)
    if response.status_code == 201:
        return 'Comment posted successfully', 200
    else:
        return 'Failed to post comment', 500

if __name__ == '__main__':
    app.run(debug=True)
