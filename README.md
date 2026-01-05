# Cinema 4D Advanced Motion Graphics Renderer

This project contains Python scripts to programmatically generate and render 3 advanced motion graphics scenes in Cinema 4D.

## Scenes

1. **Neural Pulse** - MoGraph Cloner with radial distribution, animated scale/color pulse, field-based falloff, and camera orbit animation
2. **Cosmic Collapse** - Deformer-based sphere collapse with turbulence, 3-point lighting, and depth of field
3. **AI Core** - Abstract cube lattice with step effector animation, glow material, and cinematic camera push-in

## Requirements

- Cinema 4D R25 or later
- Python (included with Cinema 4D)

## Output Specifications

- **Resolution**: 1080x1920 (Portrait)
- **Frame Rate**: 30 fps
- **Duration**: 5 seconds (150 frames)
- **Format**: MP4 (H.264)
- **Output Directory**: `./outputs/`

## Usage

### Method 1: Run from Cinema 4D Script Menu

1. Open Cinema 4D
2. Go to **Script > User Scripts > Execute Script**
3. Navigate to and select `render_all_scenes.py`
4. The script will create all three scenes and render them automatically

### Method 2: Run from Cinema 4D Python Console

1. Open Cinema 4D
2. Open the Python Console (**Window > Python Console**)
3. Run:
```python
exec(open('/Users/rajeevkumar/Downloads/cinema4d/render_all_scenes.py').read())
```

### Method 3: Command Line (if Cinema 4D CLI is available)

```bash
# Navigate to project directory
cd /Users/rajeevkumar/Downloads/cinema4d

# Run setup script (will attempt to detect Cinema 4D)
python3 setup_and_render.py
```

## File Structure

```
cinema4d/
├── scene_neural_pulse.py      # Scene A: Neural Pulse
├── scene_cosmic_collapse.py   # Scene B: Cosmic Collapse
├── scene_ai_core.py           # Scene C: AI Core
├── render_all_scenes.py       # Main render orchestrator
├── setup_and_render.py        # Setup and execution script
├── outputs/                   # Rendered MP4 files (created automatically)
│   ├── neural_pulse.mp4
│   ├── cosmic_collapse.mp4
│   └── ai_core.mp4
└── README.md                  # This file
```

## Technical Details

### Render Settings
- Renderer: Standard (falls back from Redshift if unavailable)
- Antialiasing: Geometry (lightweight)
- No Global Illumination (for faster renders)
- H.264 codec with high quality settings

### Scene Features

**Neural Pulse:**
- 50 cloned spheres in radial pattern
- Animated scale effector with field-based falloff
- Color pulse animation
- Orbiting camera

**Cosmic Collapse:**
- High-resolution sphere (64 subdivisions)
- Twist and turbulence deformers
- 3-point lighting setup (key, fill, rim)
- Depth of field enabled on camera

**AI Core:**
- 8x8x8 cube lattice (512 cubes)
- Step effector for sequential animation
- Glow material with luminance
- Slow camera push-in

## Troubleshooting

### "c4d module not found"
- Ensure you're running the script from within Cinema 4D's Python environment
- The `c4d` module is only available when running inside Cinema 4D

### Renders not completing
- Check that Cinema 4D has write permissions to the outputs directory
- Verify sufficient disk space
- Check Cinema 4D's render queue for errors

### Output files not found
- Check the `outputs/` directory
- Verify render settings are configured correctly
- Check Cinema 4D's render log for errors

## Notes

- Renders are kept short (5 seconds) for quick iteration
- All animations are deterministic and time-based
- Materials are simple to avoid heavy computation
- The script will create the `outputs/` directory if it doesn't exist

# cinema4d
