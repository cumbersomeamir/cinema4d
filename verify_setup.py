"""
Verification script to check that all required files are in place.
This can be run from system Python (doesn't require Cinema 4D).
"""

import os
import sys

def verify_setup():
    """Verify all required files exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = [
        "scene_neural_pulse.py",
        "scene_cosmic_collapse.py",
        "scene_ai_core.py",
        "render_all_scenes.py",
        "setup_and_render.py"
    ]
    
    print("=" * 60)
    print("Cinema 4D Setup Verification")
    print("=" * 60)
    
    all_present = True
    
    for filename in required_files:
        filepath = os.path.join(script_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {filename} ({size} bytes)")
        else:
            print(f"✗ {filename} - MISSING")
            all_present = False
    
    # Check outputs directory
    output_dir = os.path.join(script_dir, "outputs")
    if os.path.exists(output_dir):
        print(f"✓ outputs/ directory exists")
    else:
        print(f"⚠ outputs/ directory missing (will be created on first render)")
    
    print("=" * 60)
    
    if all_present:
        print("✓ All required files are present")
        print("\nNext steps:")
        print("1. Open Cinema 4D")
        print("2. Script > User Scripts > Execute Script")
        print("3. Select: render_all_scenes.py")
        return True
    else:
        print("✗ Some files are missing")
        return False

if __name__ == '__main__':
    success = verify_setup()
    sys.exit(0 if success else 1)

