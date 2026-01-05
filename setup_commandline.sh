#!/bin/bash
# Setup Cinema 4D Command Line Renderer

set -e

echo "============================================================"
echo "Cinema 4D Command Line Setup"
echo "============================================================"

# Find Cinema 4D installation
C4D_PATHS=(
    "/Applications/Maxon Cinema 4D 2026"
    "/Applications/Maxon Cinema 4D 2025"
    "/Applications/Maxon Cinema 4D 2024"
    "/Applications/Maxon Cinema 4D 2023"
    "/Applications/CINEMA 4D R27"
    "/Applications/CINEMA 4D R26"
    "/Applications/CINEMA 4D R25"
)

C4D_PATH=""
for path in "${C4D_PATHS[@]}"; do
    if [ -d "$path" ]; then
        C4D_PATH="$path"
        echo "✓ Found Cinema 4D at: $C4D_PATH"
        break
    fi
done

if [ -z "$C4D_PATH" ]; then
    echo "✗ Cinema 4D not found in standard locations"
    echo "Please install Cinema 4D first via Maxon App"
    exit 1
fi

# Find Commandline executable
COMMANDLINE_APP="$C4D_PATH/Commandline.app"
if [ ! -d "$COMMANDLINE_APP" ]; then
    echo "✗ Commandline.app not found at: $COMMANDLINE_APP"
    exit 1
fi

COMMANDLINE_EXE="$COMMANDLINE_APP/Contents/MacOS/Commandline"
if [ ! -f "$COMMANDLINE_EXE" ]; then
    echo "✗ Commandline executable not found"
    exit 1
fi

echo "✓ Found Commandline renderer"

# License the command line renderer (requires user interaction)
echo ""
echo "Step 1: Licensing Command Line Renderer"
echo "This will open the Commandline app for licensing..."
echo "Please follow the on-screen instructions to license it."
echo ""

# Open the commandline app for licensing
open "$COMMANDLINE_APP"

echo "Waiting for licensing to complete..."
echo "Press Enter when you've completed the licensing process..."
read

echo ""
echo "Step 2: Testing command line renderer..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Test if we can execute a simple script
if "$COMMANDLINE_EXE" -help 2>/dev/null | head -5; then
    echo "✓ Command line renderer is ready!"
    echo ""
    echo "You can now execute renders with:"
    echo "  $COMMANDLINE_EXE -script $SCRIPT_DIR/render_all_scenes.py"
else
    echo "⚠ Command line renderer may need additional setup"
fi

echo ""
echo "============================================================"
echo "Setup completed"
echo "============================================================"

