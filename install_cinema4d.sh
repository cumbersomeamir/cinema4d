#!/bin/bash
# Cinema 4D Installation Script

set -e

echo "============================================================"
echo "Cinema 4D Installation Script"
echo "============================================================"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script is for macOS only"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Step 1: Downloading Maxon App..."
# Try to get the actual download link
MAXON_DOWNLOAD_URL="https://www.maxon.net/en/downloads"

echo "Please visit $MAXON_DOWNLOAD_URL to download the Maxon App"
echo "Or we can try to download it automatically..."

# Try common download patterns
MAXON_APP_URLS=(
    "https://www.maxon.net/en/downloads/maxon-app"
    "https://www.maxon.net/en/downloads?product=maxon-app"
)

for url in "${MAXON_APP_URLS[@]}"; do
    echo "Trying: $url"
    if curl -L -f -o maxon_app.dmg "$url" 2>/dev/null; then
        if file maxon_app.dmg | grep -q "disk image"; then
            echo "✓ Successfully downloaded Maxon App"
            break
        fi
    fi
done

if [ ! -f "maxon_app.dmg" ] || ! file maxon_app.dmg | grep -q "disk image"; then
    echo "⚠ Could not auto-download. Please download manually:"
    echo "   1. Visit: https://www.maxon.net/en/downloads"
    echo "   2. Download 'Maxon App' for macOS"
    echo "   3. Save it to: $SCRIPT_DIR/maxon_app.dmg"
    echo ""
    read -p "Press Enter when you've downloaded the Maxon App DMG file..."
fi

if [ -f "maxon_app.dmg" ] && file maxon_app.dmg | grep -q "disk image"; then
    echo ""
    echo "Step 2: Mounting DMG..."
    hdiutil attach maxon_app.dmg -nobrowse -quiet
    
    echo "Step 3: Installing Maxon App..."
    # Find the app in the mounted volume
    APP_PATH=$(find /Volumes -name "Maxon App.app" -type d 2>/dev/null | head -1)
    
    if [ -n "$APP_PATH" ]; then
        echo "Found Maxon App at: $APP_PATH"
        echo "Copying to Applications..."
        cp -R "$APP_PATH" /Applications/ 2>/dev/null || sudo cp -R "$APP_PATH" /Applications/
        
        echo "Step 4: Unmounting DMG..."
        hdiutil detach /Volumes/*Maxon* 2>/dev/null || true
        
        echo ""
        echo "✓ Maxon App installed!"
        echo ""
        echo "Step 5: Next steps (requires user interaction):"
        echo "   1. Open 'Maxon App' from Applications"
        echo "   2. Sign in or create a Maxon account"
        echo "   3. Install Cinema 4D through the Maxon App"
        echo "   4. After installation, run: ./setup_commandline.sh"
        echo ""
    else
        echo "✗ Could not find Maxon App in DMG"
        exit 1
    fi
else
    echo "✗ Invalid or missing DMG file"
    exit 1
fi

echo "============================================================"
echo "Installation script completed"
echo "============================================================"

