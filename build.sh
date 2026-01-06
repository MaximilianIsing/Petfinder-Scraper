#!/bin/bash
# Build script for Render.com - installs Chrome/Chromium for Selenium

set -e

echo "Installing Chrome/Chromium for Selenium..."

# Install system dependencies
apt-get update
apt-get install -y wget gnupg ca-certificates

# Install Google Chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Verify installation
if [ -f "/usr/bin/google-chrome-stable" ]; then
    echo "Chrome installed successfully at /usr/bin/google-chrome-stable"
    /usr/bin/google-chrome-stable --version
else
    echo "Warning: Chrome installation may have failed"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build completed successfully!"

