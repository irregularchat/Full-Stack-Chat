#!/bin/bash

# Load environment variables from .env file
set -a
source /home/yourusername/Full-Stack-Chat/.env
set +a

SERVICE_PATH="/etc/systemd/system/fullstackinvite.service"
SERVICE_NAME="fullstackinvite.service"
USER=$(whoami)
WORKING_DIR="/home/$USER/Full-Stack-Chat"
ENV_PATH="/home/$USER/Full-Stack-Chat/venv/bin"
PORT=${OPEN_PORT:-5000}

# Function to create the service file called if the service does not exist
create_service_file() {
    cat <<EOF > $SERVICE_PATH
[Unit]
Description=Gunicorn instance to serve Full Stack Invite
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$WORKING_DIR
Environment="PATH=$ENV_PATH"
ExecStart=$ENV_PATH/gunicorn --workers 3 --bind 127.0.0.1:$PORT app:app

[Install]
WantedBy=multi-user.target
EOF
}

# Check if the service file exists
if [ -f "$SERVICE_PATH" ]; then
    echo "$SERVICE_NAME exists. Checking for updates..."

    # Check and update the port, username, and working directory if needed
    NEED_UPDATE=false

    if ! grep -q "ExecStart=$ENV_PATH/gunicorn --workers 3 --bind 127.0.0.1:$PORT app:app" "$SERVICE_PATH"; then
        echo "Port mismatch. Updating service file..."
        NEED_UPDATE=true
    fi

    if ! grep -q "User=$USER" "$SERVICE_PATH"; then
        echo "Username mismatch. Updating service file..."
        NEED_UPDATE=true
    fi

    if ! grep -q "WorkingDirectory=$WORKING_DIR" "$SERVICE_PATH"; then
        echo "Working directory mismatch. Updating service file..."
        NEED_UPDATE=true
    fi

    if [ "$NEED_UPDATE" = true ]; then
        echo "Updating $SERVICE_NAME..."
        create_service_file
        sudo systemctl daemon-reload
        sudo systemctl restart $SERVICE_NAME
    else
        echo "$SERVICE_NAME is up-to-date."
    fi
else
    echo "$SERVICE_NAME does not exist. Creating service file..."
    create_service_file
    sudo systemctl daemon-reload
    sudo systemctl start $SERVICE_NAME
    sudo systemctl enable $SERVICE_NAME
fi

# Ensure the service is enabled and started
if ! sudo systemctl is-enabled --quiet $SERVICE_NAME; then
    echo "Enabling $SERVICE_NAME..."
    sudo systemctl enable $SERVICE_NAME
fi

if ! sudo systemctl is-active --quiet $SERVICE_NAME; then
    echo "Starting $SERVICE_NAME..."
    sudo systemctl start $SERVICE_NAME
fi

echo "$SERVICE_NAME setup is complete."