"""
Main render orchestrator for all three scenes.
Renders each scene to MP4 format in the outputs directory.
"""

import c4d
import os
from c4d import documents, storage

# Import scene creation functions
import sys
sys.path.insert(0, os.path.dirname(__file__))

def ConfigureRenderSettings(doc, outputPath):
    """Configure render settings for MP4 output."""
    renderData = doc.GetActiveRenderData()
    
    # Set resolution (Portrait 1080x1920)
    renderData[c4d.RDATA_XRES] = 1080
    renderData[c4d.RDATA_YRES] = 1920
    renderData[c4d.RDATA_FRAMERATE] = 30.0
    
    # Set frame range
    renderData[c4d.RDATA_FRAMEFROM] = c4d.BaseTime(0)
    renderData[c4d.RDATA_FRAMETO] = c4d.BaseTime(150)
    
    # Configure video output (MP4 H.264)
    renderData[c4d.RDATA_FORMAT] = c4d.FILTER_QUICKTIME
    renderData[c4d.RDATA_SAVEIMAGE] = True
    renderData[c4d.RDATA_PATH] = outputPath
    
    # Set QuickTime/MP4 settings
    qtData = renderData[c4d.RDATA_QUICKTIME_CODEC]
    qtData[c4d.QUICKTIME_CODEC] = c4d.QUICKTIME_CODEC_H264
    qtData[c4d.QUICKTIME_QUALITY] = c4d.QUICKTIME_QUALITY_HIGH
    qtData[c4d.QUICKTIME_BITRATE] = 10000
    renderData[c4d.RDATA_QUICKTIME_CODEC] = qtData
    
    # Use Standard renderer (fallback if Redshift unavailable)
    renderData[c4d.RDATA_RENDERENGINE] = c4d.RDATA_RENDERENGINE_STANDARD
    
    # Simple render settings (no heavy GI)
    renderData[c4d.RDATA_ANTIALIASING] = c4d.ANTIALIASING_GEOMETRY
    renderData[c4d.RDATA_ANTIALIASING_MAX] = 1
    
    return renderData

def RenderScene(sceneScript, outputName):
    """Load a scene script and render it to MP4."""
    print(f"Rendering {outputName}...")
    
    # Get output directory
    scriptDir = os.path.dirname(__file__)
    outputDir = os.path.join(scriptDir, "outputs")
    os.makedirs(outputDir, exist_ok=True)
    
    outputPath = os.path.join(outputDir, outputName)
    
    # Execute scene script to create document
    try:
        # Import and execute scene creation
        if "neural_pulse" in sceneScript:
            from scene_neural_pulse import CreateNeuralPulseScene
            doc = CreateNeuralPulseScene()
        elif "cosmic_collapse" in sceneScript:
            from scene_cosmic_collapse import CreateCosmicCollapseScene
            doc = CreateCosmicCollapseScene()
        elif "ai_core" in sceneScript:
            from scene_ai_core import CreateAICoreScene
            doc = CreateAICoreScene()
        else:
            print(f"Unknown scene script: {sceneScript}")
            return None
        
        # Configure render settings
        ConfigureRenderSettings(doc, outputPath)
        
        # Render the scene
        print(f"Starting render to: {outputPath}")
        renderData = doc.GetActiveRenderData()
        
        # Execute render using RenderDocument
        # Note: This will render to the specified path
        result = c4d.documents.RenderDocument(
            doc,
            renderData,
            None,
            c4d.RENDERFLAGS_EXTERNAL
        )
        
        if result == c4d.RENDERRESULT_OK:
            print(f"Render completed: {outputPath}")
        else:
            print(f"Render completed with status: {result}")
        
        # Verify file exists
        if os.path.exists(outputPath):
            absPath = os.path.abspath(outputPath)
            print(f"✓ File verified: {absPath}")
            return absPath
        else:
            print(f"⚠ Warning: Output file not found at {outputPath}")
            return None
            
    except Exception as e:
        print(f"Error rendering {outputName}: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main execution function."""
    print("=" * 60)
    print("Cinema 4D Advanced Motion Graphics Renderer")
    print("=" * 60)
    
    # Define scenes to render
    scenes = [
        ("scene_neural_pulse.py", "neural_pulse.mp4"),
        ("scene_cosmic_collapse.py", "cosmic_collapse.mp4"),
        ("scene_ai_core.py", "ai_core.mp4")
    ]
    
    renderedFiles = []
    
    # Render each scene
    for sceneScript, outputName in scenes:
        result = RenderScene(sceneScript, outputName)
        if result:
            renderedFiles.append(result)
        print()
    
    # Print summary
    print("=" * 60)
    print("RENDER SUMMARY")
    print("=" * 60)
    if renderedFiles:
        print(f"Successfully rendered {len(renderedFiles)} scene(s):")
        for filePath in renderedFiles:
            print(f"  • {filePath}")
    else:
        print("No files were rendered successfully.")
    print("=" * 60)
    
    return renderedFiles

if __name__ == '__main__':
    main()

