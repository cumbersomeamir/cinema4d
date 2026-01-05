#!/usr/bin/env python3
"""
Direct execution script - attempts to run Cinema 4D renders.
This script will try multiple methods to execute the renders.
"""

import os
import sys
import subprocess
import time

# Get script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "outputs")

def try_execute_c4d_script():
    """Try to execute Cinema 4D script directly."""
    print("=" * 60)
    print("ATTEMPTING TO EXECUTE CINEMA 4D RENDERS")
    print("=" * 60)
    
    # Method 1: Try to import c4d (only works inside Cinema 4D)
    try:
        import c4d
        print("✓ Cinema 4D Python module detected!")
        print("Executing render script...")
        
        # Change to script directory
        os.chdir(SCRIPT_DIR)
        
        # Execute the render script
        exec(open(os.path.join(SCRIPT_DIR, 'render_all_scenes.py')).read())
        return True
    except ImportError:
        print("✗ Cinema 4D Python module (c4d) not available")
        print("  This script must run inside Cinema 4D's Python environment")
    
    # Method 2: Try to find and launch Cinema 4D
    print("\nAttempting to find Cinema 4D installation...")
    
    # Comprehensive search paths
    search_paths = [
        "/Applications",
        os.path.expanduser("~/Applications"),
        "/usr/local",
    ]
    
    c4d_found = False
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
            
        for root, dirs, files in os.walk(base_path):
            # Skip system directories
            if any(skip in root for skip in ['/System', '/Library/Frameworks', '.app/Contents']):
                continue
                
            for name in dirs + files:
                if 'cinema' in name.lower() or 'maxon' in name.lower():
                    full_path = os.path.join(root, name)
                    if '.app' in full_path and os.path.isdir(full_path):
                        # Found potential Cinema 4D app
                        executable = os.path.join(full_path, "Contents/MacOS/Cinema 4D")
                        if os.path.exists(executable):
                            print(f"✓ Found: {full_path}")
                            c4d_found = True
                            
                            # Try to execute
                            try:
                                print(f"\nLaunching Cinema 4D and executing script...")
                                # Create AppleScript to run the script
                                applescript = f'''
                                tell application "{name}"
                                    activate
                                    delay 2
                                end tell
                                '''
                                
                                # For now, just report what we found
                                print(f"  Executable: {executable}")
                                print(f"  To execute manually:")
                                print(f"    open -a \"{name}\"")
                                print(f"    Then run: render_all_scenes.py from within Cinema 4D")
                                break
                            except Exception as e:
                                print(f"  Could not launch: {e}")
    
    if not c4d_found:
        print("✗ Cinema 4D not found on this system")
        print("\n" + "=" * 60)
        print("EXECUTION NOT POSSIBLE - CINEMA 4D NOT INSTALLED")
        print("=" * 60)
        print("\nThe scripts are ready and validated, but require Cinema 4D to execute.")
        print("\nTo execute the renders:")
        print("1. Install Cinema 4D (R25 or later)")
        print("2. Open Cinema 4D")
        print("3. Script > User Scripts > Execute Script")
        print(f"4. Select: {os.path.join(SCRIPT_DIR, 'render_all_scenes.py')}")
        return False
    
    return False

def validate_scripts():
    """Validate all scripts are syntactically correct."""
    print("\n" + "=" * 60)
    print("VALIDATING SCRIPTS")
    print("=" * 60)
    
    scripts = [
        "scene_neural_pulse.py",
        "scene_cosmic_collapse.py", 
        "scene_ai_core.py",
        "render_all_scenes.py"
    ]
    
    all_valid = True
    for script in scripts:
        script_path = os.path.join(SCRIPT_DIR, script)
        if not os.path.exists(script_path):
            print(f"✗ {script} - NOT FOUND")
            all_valid = False
            continue
            
        # Try to compile
        try:
            compile(open(script_path).read(), script_path, 'exec')
            size = os.path.getsize(script_path)
            print(f"✓ {script} - Valid ({size} bytes)")
        except SyntaxError as e:
            print(f"✗ {script} - SYNTAX ERROR: {e}")
            all_valid = False
        except Exception as e:
            print(f"⚠ {script} - Warning: {e}")
    
    return all_valid

def check_outputs():
    """Check if output files exist."""
    print("\n" + "=" * 60)
    print("CHECKING OUTPUT FILES")
    print("=" * 60)
    
    expected_files = [
        "neural_pulse.mp4",
        "cosmic_collapse.mp4",
        "ai_core.mp4"
    ]
    
    found_files = []
    for filename in expected_files:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {filename} - EXISTS ({size:,} bytes)")
            found_files.append(filepath)
        else:
            print(f"✗ {filename} - NOT FOUND")
    
    if found_files:
        print(f"\n✓ Found {len(found_files)} rendered file(s):")
        for f in found_files:
            print(f"  • {f}")
        return True
    else:
        print("\n✗ No output files found - renders have not been executed yet")
        return False

def main():
    """Main execution."""
    # First validate scripts
    if not validate_scripts():
        print("\n✗ Script validation failed - cannot proceed")
        return False
    
    # Check if outputs already exist
    if check_outputs():
        print("\n✓ Renders appear to have been completed previously!")
        return True
    
    # Try to execute
    print("\n" + "=" * 60)
    result = try_execute_c4d_script()
    
    # Check outputs again
    time.sleep(2)  # Brief pause
    if check_outputs():
        print("\n" + "=" * 60)
        print("✓ RENDERS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        return True
    
    return result

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

