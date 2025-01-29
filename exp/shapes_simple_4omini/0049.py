import bpy

def create_cross(size=1, location=(0, 0, 0)):
    # Create the horizontal arm of the cross
    bpy.ops.mesh.primitive_cube_add(size=size, location=(location[0], location[1] + size/2, location[2]))
    horizontal_arm = bpy.context.object
    horizontal_arm.scale[1] = 0.1  # Make it thin
    
    # Create the vertical arm of the cross
    bpy.ops.mesh.primitive_cube_add(size=size, location=(location[0] + size/2, location[1], location[2]))
    vertical_arm = bpy.context.object
    vertical_arm.scale[0] = 0.1  # Make it thin

create_cross(size=2, location=(0, 0, 0))