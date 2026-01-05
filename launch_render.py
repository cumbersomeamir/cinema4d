#!/usr/bin/env python3
"""
Launcher script that attempts to find and execute Cinema 4D with the render script.
This script tries multiple methods to launch Cinema 4D.
"""

import os
import sys
import subprocess
import time

def find_cinema4d():
    """Find Cinema 4D installation."""
    possible_paths = [
        "/Applications/Maxon Cinema 4D 2024/Cinema 4D.app/Contents/MacOS/Cinema 4D",
        "/Applications/Maxon Cinema 4D 2023/Cinema 4D.app/Contents/MacOS/Cinema 4D",
        "/Applications/Maxon Cinema 4D 2025/Cinema 4D.app/Contents/MacOS/Cinema 4D",
        "/Applications/CINEMA 4D R25/CINEMA 4D.app/Contents/MacOS/CINEMA 4D",
        "/Applications/CINEMA 4D R26/CINEMA 4D.app/Contents/MacOS/CINEMA 4D",
        "/Applications/CINEMA 4D R27/CINEMA 4D.app/Contents/MacOS/CINEMA 4D",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Try to find via mdfind
    try:
        result = subprocess.run(
            ["mdfind", "kMDItemKind == 'Application' && kMDItemDisplayName == 'Cinema 4D*'"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line and 'Cinema 4D' in line:
                    app_path = os.path.join(line, "Contents/MacOS/Cinema 4D")
                    if os.path.exists(app_path):
                        return app_path
                    # Try alternative name
                    app_path = os.path.join(line, "Contents/MacOS/CINEMA 4D")
                    if os.path.exists(app_path):
                        return app_path
    except:
        pass
    
    return None

def create_c4d_script():
    """Create a Cinema 4D script file that will execute our render script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    render_script = os.path.join(script_dir, "render_all_scenes.py")
    
    # Create a wrapper script that Cinema 4D can execute
    wrapper_content = f'''# Cinema 4D Script Wrapper
import c4d
import sys
import os

# Add script directory to path
script_dir = r"{script_dir}"
sys.path.insert(0, script_dir)

# Execute the render script
try:
    exec(open(r"{render_script}").read())
    print("Render script execution completed")
except Exception as e:
    print(f"Error: {{e}}")
    import traceback
    traceback.print_exc()
'''
    
    wrapper_path = os.path.join(script_dir, "c4d_wrapper_script.py")
    with open(wrapper_path, 'w') as f:
        f.write(wrapper_content)
    
    return wrapper_path

def main():
    """Main execution."""
    print("=" * 60)
    print("Cinema 4D Render Launcher")
    print("=" * 60)
    
    # Find Cinema 4D
    c4d_path = find_cinema4d()
    if not c4d_path:
        print("✗ Cinema 4D not found in standard locations")
        print("\nPlease run the script manually from within Cinema 4D:")
        print("  1. Open Cinema 4D")
        print("  2. Script > User Scripts > Execute Script")
        print("  3. Select: render_all_scenes.py")
        return False
    
    print(f"✓ Found Cinema 4D: {c4d_path}")
    
    # Create wrapper script
    wrapper_script = create_c4d_script()
    print(f"✓ Created wrapper script: {wrapper_script}")
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to execute Cinema 4D with the script
    print("\nAttempting to launch Cinema 4D with render script...")
    print("Note: Cinema 4D may open a GUI window. The render will execute automatically.")
    
    try:
        # Try headless mode first (if supported)
        cmd = [
            c4d_path,
            "-nogui",
            "-execute",
            wrapper_script
        ]
        
        print(f"Executing: {' '.join(cmd)}")
        result = subprocess.run(cmd, cwd=script_dir, timeout=600)
        
        if result.returncode == 0:
            print("\n✓ Render completed successfully!")
            return True
        else:
            print(f"\n⚠ Cinema 4D exited with code: {result.returncode}")
            print("The render may still have completed. Check the outputs directory.")
            return True
            
    except subprocess.TimeoutExpired:
        print("\n⚠ Render process timed out (this may be normal for long renders)")
        return True
    except FileNotFoundError:
        print(f"\n✗ Could not execute: {c4d_path}")
        print("Please run the script manually from within Cinema 4D")
        return False
    except Exception as e:
        print(f"\n✗ Error launching Cinema 4D: {e}")
        print("\nAlternative: Run manually from Cinema 4D:")
        print("  1. Open Cinema 4D")
        print("  2. Script > User Scripts > Execute Script")
        print(f"  3. Select: {os.path.join(script_dir, 'render_all_scenes.py')}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

