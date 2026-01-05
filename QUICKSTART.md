# Quick Start Guide

## Immediate Execution

To render all three scenes immediately:

1. **Open Cinema 4D** (R25 or later)

2. **Execute the render script:**
   - Go to: **Script > User Scripts > Execute Script**
   - Navigate to: `/Users/rajeevkumar/Downloads/cinema4d/`
   - Select: `render_all_scenes.py`
   - Click **Execute**

3. **Wait for renders to complete** (approximately 5-10 minutes depending on hardware)

4. **Find your videos:**
   - Location: `/Users/rajeevkumar/Downloads/cinema4d/outputs/`
   - Files:
     - `neural_pulse.mp4`
     - `cosmic_collapse.mp4`
     - `ai_core.mp4`

## Alternative: Python Console Method

1. Open Cinema 4D
2. Open Python Console: **Window > Python Console**
3. Paste and execute:
```python
import sys
sys.path.insert(0, '/Users/rajeevkumar/Downloads/cinema4d')
exec(open('/Users/rajeevkumar/Downloads/cinema4d/render_all_scenes.py').read())
```

## What Gets Rendered

### Scene A: Neural Pulse
- **Duration**: 5 seconds (150 frames @ 30fps)
- **Features**: Radial MoGraph cloner, animated scale pulse, color effects, orbiting camera
- **Output**: `outputs/neural_pulse.mp4`

### Scene B: Cosmic Collapse
- **Duration**: 5 seconds (150 frames @ 30fps)
- **Features**: Twisting sphere with turbulence, 3-point lighting, depth of field
- **Output**: `outputs/cosmic_collapse.mp4`

### Scene C: AI Core
- **Duration**: 5 seconds (150 frames @ 30fps)
- **Features**: Cube lattice with step animation, glow material, camera push-in
- **Output**: `outputs/ai_core.mp4`

## Troubleshooting

**"c4d module not found"**
- You must run scripts from within Cinema 4D's Python environment
- System Python cannot access the c4d module

**Renders not starting**
- Check that Cinema 4D has write permissions to the outputs directory
- Verify render settings are configured (should be automatic)

**Output files missing**
- Check Cinema 4D's render queue for errors
- Verify the outputs directory path is correct
- Check disk space availability

## File Locations

- **Scripts**: `/Users/rajeevkumar/Downloads/cinema4d/`
- **Outputs**: `/Users/rajeevkumar/Downloads/cinema4d/outputs/`

## Notes

- Renders use Standard renderer (fast, no heavy GI)
- All scenes are optimized for quick rendering
- Portrait format (1080x1920) for vertical video
- H.264 codec for compatibility

