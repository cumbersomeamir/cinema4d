"""
Scene C: AI Core
- Abstract cube lattice
- Step effector animation
- Glow-style material
- Slow cinematic camera push-in
"""

import c4d
from c4d import documents, plugins, utils, bitmaps, gui

def CreateAICoreScene():
    """Create the AI Core scene with cube lattice and step effector."""
    
    # Create new document
    doc = documents.BaseDocument()
    doc.SetFps(30)
    
    # Set render settings - Portrait 1080x1920
    renderData = doc.GetActiveRenderData()
    renderData[c4d.RDATA_XRES] = 1080
    renderData[c4d.RDATA_YRES] = 1920
    renderData[c4d.RDATA_FRAMERATE] = 30.0
    renderData[c4d.RDATA_FRAMEFROM] = c4d.BaseTime(0)
    renderData[c4d.RDATA_FRAMETO] = c4d.BaseTime(150)
    
    # Create base cube for lattice
    cube = c4d.BaseObject(c4d.Ocube)
    cube[c4d.PRIM_CUBE_LEN] = c4d.Vector(30, 30, 30)
    cube.SetName("LatticeCube")
    
    # Create MoGraph Cloner for lattice structure
    cloner = c4d.BaseObject(c4d.Ocloner)
    cloner[c4d.MGCLONER_MODE] = c4d.MGCLONER_MODE_GRIDARRAY
    cloner[c4d.MGCLONER_COUNT] = c4d.Vector(8, 8, 8)
    cloner[c4d.MGCLONER_SIZE] = c4d.Vector(400, 400, 400)
    cube.InsertUnder(cloner)
    doc.InsertObject(cloner)
    
    # Create Step Effector for animation
    stepEffector = c4d.BaseObject(c4d.Omgshader)
    stepEffector[c4d.MGSHADER_SHADER] = c4d.MGSHADER_SHADER_STEP
    stepEffector[c4d.MGSHADER_STEP_STEPS] = 10
    stepEffector[c4d.MGSHADER_STEP_START] = 0
    stepEffector[c4d.MGSHADER_STEP_END] = 100
    stepEffector[c4d.MGSHADER_STRENGTH] = 1.0
    
    # Animate step effector
    doc.SetTime(c4d.BaseTime(0))
    stepEffector[c4d.MGSHADER_STEP_START] = 0
    stepEffector[c4d.MGSHADER_STEP_END] = 0
    doc.AnimateObject(stepEffector, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    stepEffector[c4d.MGSHADER_STEP_START] = 0
    stepEffector[c4d.MGSHADER_STEP_END] = 100
    doc.AnimateObject(stepEffector, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.InsertObject(stepEffector)
    cloner.InsertEffector(stepEffector)
    
    # Create glow material
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(0.0, 0.8, 1.0)
    mat[c4d.MATERIAL_USE_LUMINANCE] = True
    mat[c4d.MATERIAL_LUMINANCE_COLOR] = c4d.Vector(0.0, 0.9, 1.0)
    mat[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = 150
    mat[c4d.MATERIAL_USE_GLOW] = True
    mat[c4d.MATERIAL_GLOW_COLOR] = c4d.Vector(0.0, 0.8, 1.0)
    mat[c4d.MATERIAL_GLOW_INTENSITY] = 200
    matName = doc.InsertMaterial(mat)
    
    # Apply material
    tag = c4d.BaseTag(c4d.Ttexture)
    tag[c4d.TEXTURETAG_MATERIAL] = mat
    cube.InsertTag(tag)
    
    # Create camera with slow push-in
    cam = c4d.BaseObject(c4d.Ocamera)
    cam[c4d.CAMERAOBJECT_APERTURE] = 36
    cam[c4d.CAMERA_PROJECTION] = c4d.PERSPECTIVE
    cam.SetAbsPos(c4d.Vector(0, 0, 1200))
    cam.SetAbsRot(c4d.Vector(0, 0, 0))
    
    # Animate slow push-in
    doc.SetTime(c4d.BaseTime(0))
    cam.SetAbsPos(c4d.Vector(0, 0, 1200))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    cam.SetAbsPos(c4d.Vector(0, 0, 600))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.InsertObject(cam)
    doc.SetActiveObject(cam, c4d.SELECTION_NEW)
    
    # Add ambient light
    light = c4d.BaseObject(c4d.Olight)
    light[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    light[c4d.LIGHT_BRIGHTNESS] = 80
    light[c4d.LIGHT_COLOR] = c4d.Vector(0.8, 0.9, 1.0)
    light.SetAbsPos(c4d.Vector(0, 0, 500))
    doc.InsertObject(light)
    
    # Add rim light for depth
    rimLight = c4d.BaseObject(c4d.Olight)
    rimLight[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    rimLight[c4d.LIGHT_BRIGHTNESS] = 60
    rimLight[c4d.LIGHT_COLOR] = c4d.Vector(0.0, 0.6, 1.0)
    rimLight.SetAbsPos(c4d.Vector(-400, -400, -400))
    doc.InsertObject(rimLight)
    
    doc.SetTime(c4d.BaseTime(0))
    
    return doc

def main():
    """Main execution function."""
    doc = CreateAICoreScene()
    documents.InsertDocument(doc)
    c4d.EventAdd()
    return doc

if __name__ == '__main__':
    main()

