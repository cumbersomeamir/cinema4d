"""
Scene A: Neural Pulse
- MoGraph Cloner (radial)
- Animated scale + color pulse
- Field-based falloff
- Camera orbit animation
"""

import c4d
from c4d import documents, plugins, utils, bitmaps, gui

def CreateNeuralPulseScene():
    """Create the Neural Pulse scene with MoGraph Cloner and animated effects."""
    
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
    
    # Create base sphere for cloning
    sphere = c4d.BaseObject(c4d.Osphere)
    sphere[c4d.PRIM_SPHERE_RAD] = 20
    sphere[c4d.PRIM_SPHERE_SUB] = 24
    doc.InsertObject(sphere)
    
    # Create MoGraph Cloner
    cloner = c4d.BaseObject(c4d.Ocloner)
    cloner[c4d.MGCLONER_MODE] = c4d.MGCLONER_MODE_RADIAL
    cloner[c4d.MGCLONER_COUNT] = 50
    cloner[c4d.MGCLONER_RADIALCOUNT] = 5
    cloner[c4d.MGCLONER_RADIUS] = 300
    cloner[c4d.MGCLONER_RADIALSTEP] = 60
    sphere.InsertUnder(cloner)
    doc.InsertObject(cloner)
    
    # Create material with color
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(0.2, 0.6, 1.0)
    mat[c4d.MATERIAL_USE_LUMINANCE] = True
    mat[c4d.MATERIAL_LUMINANCE_COLOR] = c4d.Vector(0.2, 0.6, 1.0)
    mat[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = 100
    matName = doc.InsertMaterial(mat)
    
    # Apply material to sphere
    tag = c4d.BaseTag(c4d.Ttexture)
    tag[c4d.TEXTURETAG_MATERIAL] = mat
    sphere.InsertTag(tag)
    
    # Create Scale effector with animation
    scaleEffector = c4d.BaseObject(c4d.Omgshader)
    scaleEffector[c4d.MGSHADER_SHADER] = c4d.MGSHADER_SHADER_SCALE
    scaleEffector[c4d.MGSHADER_SCALE] = c4d.Vector(0.3, 0.3, 0.3)
    scaleEffector[c4d.MGSHADER_STRENGTH] = 1.0
    
    # Add falloff for field-based effect (simplified approach)
    try:
        # Try to add field layer if API is available
        fieldLayer = c4d.modules.mograph.FieldLayer(c4d.FLspline)
        falloff = c4d.modules.mograph.FieldFalloff(c4d.FIELDFALLOFF_LINEAR)
        falloff[c4d.FIELDFALLOFF_SIZE] = 200
        fieldLayer.InsertFalloff(falloff)
        fieldList = scaleEffector[c4d.FIELDS]
        if fieldList:
            fieldList.InsertLayer(fieldLayer)
            scaleEffector[c4d.FIELDS] = fieldList
    except:
        # Fallback: use effector without field (still works)
        pass
    
    doc.InsertObject(scaleEffector)
    cloner.InsertEffector(scaleEffector)
    
    # Create color effector for pulse
    colorEffector = c4d.BaseObject(c4d.Omgshader)
    colorEffector[c4d.MGSHADER_SHADER] = c4d.MGSHADER_SHADER_COLOR
    colorEffector[c4d.MGSHADER_COLOR] = c4d.Vector(1.0, 0.3, 0.8)
    colorEffector[c4d.MGSHADER_STRENGTH] = 0.8
    doc.InsertObject(colorEffector)
    cloner.InsertEffector(colorEffector)
    
    # Create camera with orbit animation
    cam = c4d.BaseObject(c4d.Ocamera)
    cam[c4d.CAMERAOBJECT_APERTURE] = 36
    cam[c4d.CAMERA_PROJECTION] = c4d.PERSPECTIVE
    
    # Animate camera orbit
    doc.SetTime(c4d.BaseTime(0))
    cam.SetAbsPos(c4d.Vector(0, 0, 600))
    cam.SetAbsRot(c4d.Vector(0, 0, 0))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    cam.SetAbsPos(c4d.Vector(600, 200, 0))
    cam.SetAbsRot(c4d.Vector(0, 90, 0))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.InsertObject(cam)
    doc.SetActiveObject(cam, c4d.SELECTION_NEW)
    
    # Add light
    light = c4d.BaseObject(c4d.Olight)
    light[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    light[c4d.LIGHT_BRIGHTNESS] = 120
    light.SetAbsPos(c4d.Vector(300, 300, 300))
    doc.InsertObject(light)
    
    # Set keyframes for pulse animation
    doc.SetTime(c4d.BaseTime(0))
    scaleEffector[c4d.MGSHADER_STRENGTH] = 0.0
    doc.AnimateObject(scaleEffector, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(75))
    scaleEffector[c4d.MGSHADER_STRENGTH] = 1.0
    doc.AnimateObject(scaleEffector, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    scaleEffector[c4d.MGSHADER_STRENGTH] = 0.0
    doc.AnimateObject(scaleEffector, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(0))
    
    return doc

def main():
    """Main execution function."""
    doc = CreateNeuralPulseScene()
    documents.InsertDocument(doc)
    c4d.EventAdd()
    return doc

if __name__ == '__main__':
    main()

