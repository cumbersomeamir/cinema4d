# Cinema 4D Auto-Installation Guide

## Current Status

Cinema 4D requires manual installation through the Maxon App, which needs:
1. User account creation/login
2. License acceptance (EULA)
3. User interaction for installation

## What I've Prepared

✅ All Cinema 4D Python scripts are ready and validated
✅ Output directory created
✅ Installation scripts prepared
✅ Command line setup scripts ready

## Manual Installation Steps

Since Cinema 4D installation requires user interaction, please follow these steps:

### Step 1: Download Maxon App

1. Visit: https://www.maxon.net/en/downloads
2. Click "Download Maxon App 2026.1.0" (or latest version)
3. Save the DMG file

### Step 2: Install Maxon App

```bash
cd /Users/rajeevkumar/Downloads/cinema4d
# Mount and install the DMG
hdiutil attach ~/Downloads/MaxonApp*.dmg
cp -R /Volumes/Maxon\ App/Maxon\ App.app /Applications/
hdiutil detach /Volumes/Maxon\ App
```

### Step 3: Install Cinema 4D

1. Open "Maxon App" from Applications
2. Sign in or create a Maxon account
3. Accept the EULA
4. Click "Install" next to Cinema 4D
5. Wait for installation to complete

### Step 4: License Command Line Renderer

```bash
cd /Users/rajeevkumar/Downloads/cinema4d
./setup_commandline.sh
```

### Step 5: Execute Renders

Once Cinema 4D is installed and command line is licensed:

```bash
cd /Users/rajeevkumar/Downloads/cinema4d

# Find Cinema 4D commandline
C4D_CMD="/Applications/Maxon Cinema 4D 2026/Commandline.app/Contents/MacOS/Commandline"

# Execute renders
"$C4D_CMD" -script render_all_scenes.py
```

Or from within Cinema 4D GUI:
1. Open Cinema 4D
2. Script > User Scripts > Execute Script
3. Select: `render_all_scenes.py`

## Alternative: Use Cinema 4D Trial

Maxon offers a free trial. You can:
1. Download Maxon App (free)
2. Sign up for a free trial account
3. Install Cinema 4D trial
4. Use it for 14 days (fully functional)

## Expected Output

After successful execution, you'll find:
- `/Users/rajeevkumar/Downloads/cinema4d/outputs/neural_pulse.mp4`
- `/Users/rajeevkumar/Downloads/cinema4d/outputs/cosmic_collapse.mp4`
- `/Users/rajeevkumar/Downloads/cinema4d/outputs/ai_core.mp4`

Each video will be:
- 1080x1920 (Portrait)
- 30 fps
- 5 seconds (150 frames)
- MP4 H.264 format

