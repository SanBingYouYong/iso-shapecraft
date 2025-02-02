import bpy

def create_serving_tray(length=2, width=1, height=0.1, side_height=0.05):
    # Create the base of the tray
    bpy.ops.mesh.primitive_plane_add(size=length, location=(0, 0, height))
    base = bpy.context.object
    base.name = "ServingTrayBase"
    
    # Create the sides of the tray
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(length / 2, 0, height + side_height / 2))
    side1 = bpy.context.object
    side1.name = "TraySide1"
    side1.scale[0] = length / 2
    side1.scale[1] = side_height / 2
    side1.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(-length / 2, 0, height + side_height / 2))
    side2 = bpy.context.object
    side2.name = "TraySide2"
    side2.scale[0] = length / 2
    side2.scale[1] = side_height / 2
    side2.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, width / 2, height + side_height / 2))
    side3 = bpy.context.object
    side3.name = "TraySide3"
    side3.scale[0] = width / 2
    side3.scale[1] = side_height / 2
    side3.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, -width / 2, height + side_height / 2))
    side4 = bpy.context.object
    side4.name = "TraySide4"
    side4.scale[0] = width / 2
    side4.scale[1] = side_height / 2
    side4.scale[2] = side_height

create_serving_tray()