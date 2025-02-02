import bpy

def create_serving_tray(length=1.5, width=0.75, base_height=0.02, side_height=0.05):
    # Create the base of the tray
    bpy.ops.mesh.primitive_plane_add(size=length, location=(0, 0, base_height))
    base = bpy.context.object
    base.name = "ServingTrayBase"
    
    # Create the sides of the tray
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(length / 2, 0, base_height + side_height / 2))
    side1 = bpy.context.object
    side1.name = "TraySide1"
    side1.scale[0] = length / 2
    side1.scale[1] = 0.01  # Thin side
    side1.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(-length / 2, 0, base_height + side_height / 2))
    side2 = bpy.context.object
    side2.name = "TraySide2"
    side2.scale[0] = length / 2
    side2.scale[1] = 0.01  # Thin side
    side2.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, width / 2, base_height + side_height / 2))
    side3 = bpy.context.object
    side3.name = "TraySide3"
    side3.scale[0] = 0.01  # Thin side
    side3.scale[1] = width / 2
    side3.scale[2] = side_height
    
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, -width / 2, base_height + side_height / 2))
    side4 = bpy.context.object
    side4.name = "TraySide4"
    side4.scale[0] = 0.01  # Thin side
    side4.scale[1] = width / 2
    side4.scale[2] = side_height

create_serving_tray()