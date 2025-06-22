# Deployment Guide

This guide helps you deploy the Full-Stack-Chat webhook service.

## Prerequisites
- Python 3.7+
- GitHub account with personal access token
- A domain or ngrok for webhook URL

## Quick Start

1. Clone the repository
2. Copy `.env-template` to `.env` and fill in your values
3. Install dependencies: `pip install -r requirements.txt`
4. Run locally: `python fullstack-invite.py`
5. For production on Linux: `./production-run.sh`

## Configuration

- `GITHUB_TOKEN`: Personal access token with repo permissions
- `GITHUB_SECRET`: Webhook secret for verification
- `REPO_NAME`: Full repository path (e.g., username/repo)
- `SIGNAL_INVITE_LINK`: Your Signal group invite URL
- `OPEN_PORT`: Port for the Flask application

## Testing

Use `test.py` to verify your webhook is working correctly.