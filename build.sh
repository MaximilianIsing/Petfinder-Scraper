#!/bin/bash
# Build script for Render.com - installs Chrome/Chromium for Selenium

set +e  # Don't exit on error - continue even if Chrome installation fails

echo "Installing Python dependencies first..."
pip install -r requirements.txt

echo "Attempting to install Chrome for Selenium..."

# Try to install Chrome - this may fail on Render's read-only filesystem
# If it fails, the /scrape endpoint will still work, but /scrape-js won't

# Method 1: Try apt-get (may fail on Render)
if command -v apt-get &> /dev/null; then
    echo "Trying apt-get method..."
    apt-get update 2>&1 | grep -v "Read-only file system" || true
    if [ $? -eq 0 ] || [ $? -eq 1 ]; then
        apt-get install -y wget gnupg ca-certificates 2>&1 | grep -v "Read-only file system" || true
        
        # Add Chrome repository
        wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub 2>/dev/null | apt-key add - 2>/dev/null || true
        echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /tmp/google-chrome.list 2>/dev/null || true
        cat /tmp/google-chrome.list >> /etc/apt/sources.list.d/google-chrome.list 2>/dev/null || true
        
        apt-get update 2>&1 | grep -v "Read-only file system" || true
        apt-get install -y google-chrome-stable 2>&1 | grep -v "Read-only file system" || true
    fi
fi

# Method 2: Download Chrome binary directly to user directory
if [ ! -f "/usr/bin/google-chrome-stable" ] && [ ! -f "$HOME/bin/google-chrome-stable" ]; then
    echo "Chrome not found in system paths. Trying direct download..."
    
    CHROME_DIR="$HOME/chrome"
    mkdir -p "$CHROME_DIR" 2>/dev/null || true
    
    if command -v wget &> /dev/null; then
        wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O "$CHROME_DIR/chrome.deb" 2>/dev/null || true
        
        if [ -f "$CHROME_DIR/chrome.deb" ] && command -v dpkg-deb &> /dev/null; then
            echo "Extracting Chrome from deb package..."
            cd "$CHROME_DIR"
            dpkg-deb -x chrome.deb . 2>/dev/null || true
            
            if [ -f "$CHROME_DIR/opt/google/chrome/chrome" ]; then
                mkdir -p "$HOME/bin" 2>/dev/null || true
                cp "$CHROME_DIR/opt/google/chrome/chrome" "$HOME/bin/google-chrome-stable" 2>/dev/null || true
                chmod +x "$HOME/bin/google-chrome-stable" 2>/dev/null || true
                export PATH="$HOME/bin:$PATH"
                echo "Chrome extracted to $HOME/bin/google-chrome-stable"
            fi
        fi
    fi
fi

# Verify Chrome installation
CHROME_FOUND=false
if [ -f "/usr/bin/google-chrome-stable" ]; then
    echo "✓ Chrome found at /usr/bin/google-chrome-stable"
    CHROME_FOUND=true
elif [ -f "$HOME/bin/google-chrome-stable" ]; then
    echo "✓ Chrome found at $HOME/bin/google-chrome-stable"
    CHROME_FOUND=true
elif command -v google-chrome-stable &> /dev/null; then
    echo "✓ Chrome found in PATH"
    CHROME_FOUND=true
fi

if [ "$CHROME_FOUND" = false ]; then
    echo "⚠ Warning: Chrome not found. /scrape-js endpoint will not work."
    echo "  Standard /scrape endpoint will still function normally."
    echo "  To enable /scrape-js, Chrome needs to be installed."
else
    echo "✓ Chrome installation successful - /scrape-js endpoint is ready"
fi

echo "Build completed!"
