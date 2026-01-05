"""
Scene B: Cosmic Collapse
- Deformer-based sphere collapse
- Turbulence + time-based noise
- Dramatic lighting (3-point)
- Depth of field enabled
"""

import c4d
from c4d import documents, plugins, utils, bitmaps, gui

def CreateCosmicCollapseScene():
    """Create the Cosmic Collapse scene with deformer and turbulence."""
    
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
    
    # Create high-res sphere for collapse
    sphere = c4d.BaseObject(c4d.Osphere)
    sphere[c4d.PRIM_SPHERE_RAD] = 200
    sphere[c4d.PRIM_SPHERE_SUB] = 64
    sphere.SetName("CollapseSphere")
    doc.InsertObject(sphere)
    
    # Create Twist deformer for collapse effect
    twist = c4d.BaseObject(c4d.Otwist)
    twist[c4d.TWISTOBJECT_ANGLE] = 0
    twist[c4d.TWISTOBJECT_SIZE] = 400
    twist.InsertUnder(sphere)
    
    # Animate twist
    doc.SetTime(c4d.BaseTime(0))
    twist[c4d.TWISTOBJECT_ANGLE] = 0
    doc.AnimateObject(twist, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    twist[c4d.TWISTOBJECT_ANGLE] = 720
    doc.AnimateObject(twist, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    # Create Turbulence deformer
    turbulence = c4d.BaseObject(c4d.Oturbulence)
    turbulence[c4d.TURBULENCEOBJECT_STRENGTH] = 50
    turbulence[c4d.TURBULENCEOBJECT_SCALE] = 0.5
    turbulence[c4d.TURBULENCEOBJECT_SPEED] = 0.1
    turbulence.InsertUnder(sphere)
    
    # Animate turbulence strength
    doc.SetTime(c4d.BaseTime(0))
    turbulence[c4d.TURBULENCEOBJECT_STRENGTH] = 20
    doc.AnimateObject(turbulence, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    turbulence[c4d.TURBULENCEOBJECT_STRENGTH] = 100
    doc.AnimateObject(turbulence, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    # Create material with dark cosmic look
    mat = c4d.BaseMaterial(c4d.Mmaterial)
    mat[c4d.MATERIAL_USE_COLOR] = True
    mat[c4d.MATERIAL_COLOR_COLOR] = c4d.Vector(0.1, 0.1, 0.3)
    mat[c4d.MATERIAL_USE_LUMINANCE] = True
    mat[c4d.MATERIAL_LUMINANCE_COLOR] = c4d.Vector(0.4, 0.2, 0.8)
    mat[c4d.MATERIAL_LUMINANCE_BRIGHTNESS] = 80
    mat[c4d.MATERIAL_USE_REFLECTION] = True
    mat[c4d.MATERIAL_REFLECTION_REFLECTANCE] = 0.3
    matName = doc.InsertMaterial(mat)
    
    # Apply material
    tag = c4d.BaseTag(c4d.Ttexture)
    tag[c4d.TEXTURETAG_MATERIAL] = mat
    sphere.InsertTag(tag)
    
    # 3-Point Lighting Setup
    # Key light (main)
    keyLight = c4d.BaseObject(c4d.Olight)
    keyLight[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    keyLight[c4d.LIGHT_BRIGHTNESS] = 150
    keyLight[c4d.LIGHT_COLOR] = c4d.Vector(1.0, 0.9, 0.8)
    keyLight.SetAbsPos(c4d.Vector(300, 400, 300))
    doc.InsertObject(keyLight)
    
    # Fill light (softer)
    fillLight = c4d.BaseObject(c4d.Olight)
    fillLight[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    fillLight[c4d.LIGHT_BRIGHTNESS] = 80
    fillLight[c4d.LIGHT_COLOR] = c4d.Vector(0.6, 0.7, 1.0)
    fillLight.SetAbsPos(c4d.Vector(-300, 200, -200))
    doc.InsertObject(fillLight)
    
    # Rim light (back)
    rimLight = c4d.BaseObject(c4d.Olight)
    rimLight[c4d.LIGHT_TYPE] = c4d.LIGHT_TYPE_OMNI
    rimLight[c4d.LIGHT_BRIGHTNESS] = 100
    rimLight[c4d.LIGHT_COLOR] = c4d.Vector(0.8, 0.4, 1.0)
    rimLight.SetAbsPos(c4d.Vector(0, 0, -500))
    doc.InsertObject(rimLight)
    
    # Create camera with depth of field
    cam = c4d.BaseObject(c4d.Ocamera)
    cam[c4d.CAMERAOBJECT_APERTURE] = 36
    cam[c4d.CAMERA_PROJECTION] = c4d.PERSPECTIVE
    cam[c4d.CAMERA_FOCUS] = 600
    cam[c4d.CAMERAOBJECT_FOCUS] = 600
    cam[c4d.CAMERAOBJECT_TARGETOBJECT] = sphere
    
    # Enable depth of field
    cam[c4d.CAMERA_DOF_ENABLED] = True
    cam[c4d.CAMERA_DOF_FOCAL_DISTANCE] = 600
    cam[c4d.CAMERA_DOF_FSTOP] = 2.8
    
    cam.SetAbsPos(c4d.Vector(0, 0, 800))
    cam.SetAbsRot(c4d.Vector(0, 0, 0))
    doc.InsertObject(cam)
    doc.SetActiveObject(cam, c4d.SELECTION_NEW)
    
    # Animate camera slight movement
    doc.SetTime(c4d.BaseTime(0))
    cam.SetAbsPos(c4d.Vector(0, 0, 800))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(150))
    cam.SetAbsPos(c4d.Vector(50, 30, 750))
    doc.AnimateObject(cam, doc.GetTime(), c4d.ANIMATEFLAGS_0)
    
    doc.SetTime(c4d.BaseTime(0))
    
    return doc

def main():
    """Main execution function."""
    doc = CreateCosmicCollapseScene()
    documents.InsertDocument(doc)
    c4d.EventAdd()
    return doc

if __name__ == '__main__':
    main()

