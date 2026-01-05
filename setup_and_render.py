"""
Setup script that detects Cinema 4D environment and executes renders.
This script can be run from Cinema 4D's Python console or command line.
"""

import os
import sys
import subprocess

def DetectCinema4D():
    """Detect Cinema 4D installation path."""
    possible_paths = [
        "/Applications/Maxon Cinema 4D 2024/Cinema 4D.app",
        "/Applications/Maxon Cinema 4D 2023/Cinema 4D.app",
        "/Applications/Maxon Cinema 4D 2025/Cinema 4D.app",
        "/Applications/CINEMA 4D R25/CINEMA 4D.app",
        "/Applications/CINEMA 4D R26/CINEMA 4D.app",
        "/Applications/CINEMA 4D R27/CINEMA 4D.app",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Try to find via mdfind (macOS Spotlight)
    try:
        result = subprocess.run(
            ["mdfind", "kMDItemKind == 'Application' && kMDItemDisplayName == 'Cinema 4D*'"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None

def VerifyC4DModule():
    """Verify c4d Python module is available."""
    try:
        import c4d
        print(f"✓ Cinema 4D Python module available (version: {c4d.__version__ if hasattr(c4d, '__version__') else 'unknown'})")
        return True
    except ImportError:
        print("✗ Cinema 4D Python module (c4d) not available")
        print("  This script must be run within Cinema 4D's Python environment")
        return False

def CreateOutputDirectory():
    """Create outputs directory if missing."""
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    outputDir = os.path.join(scriptDir, "outputs")
    os.makedirs(outputDir, exist_ok=True)
    print(f"✓ Output directory ready: {outputDir}")
    return outputDir

def main():
    """Main setup and execution."""
    print("=" * 60)
    print("Cinema 4D Environment Setup")
    print("=" * 60)
    
    # Step 1: Detect Cinema 4D
    c4d_path = DetectCinema4D()
    if c4d_path:
        print(f"✓ Cinema 4D detected: {c4d_path}")
    else:
        print("⚠ Cinema 4D not found in standard locations")
        print("  Continuing anyway (may be installed elsewhere)")
    
    # Step 2: Verify c4d module
    if not VerifyC4DModule():
        print("\nERROR: Cannot proceed without Cinema 4D Python module")
        print("Please run this script from within Cinema 4D:")
        print("  1. Open Cinema 4D")
        print("  2. Script > User Scripts > Execute Script")
        print("  3. Select: render_all_scenes.py")
        return False
    
    # Step 3: Create outputs directory
    outputDir = CreateOutputDirectory()
    
    print("\n" + "=" * 60)
    print("Environment setup complete. Starting renders...")
    print("=" * 60 + "\n")
    
    # Step 4: Execute renders
    try:
        from render_all_scenes import main as render_main
        renderedFiles = render_main()
        
        if renderedFiles:
            print("\n✓ All renders completed successfully!")
            return True
        else:
            print("\n⚠ Some renders may have failed")
            return False
            
    except Exception as e:
        print(f"\n✗ Error during rendering: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

