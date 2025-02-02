import bpy

def create_chair():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the seat
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
    seat = bpy.context.object
    seat.scale[0] = 1.0  # Width
    seat.scale[1] = 1.0  # Depth
    seat.scale[2] = 0.2  # Height

    # Create the backrest
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.55, 1))
    backrest = bpy.context.object
    backrest.scale[0] = 1.0  # Width
    backrest.scale[1] = 0.1  # Depth
    backrest.scale[2] = 0.6  # Height

    # Create the legs
    leg_positions = [
        (-0.9, -0.9, 0.2),  # Front-left
        (0.9, -0.9, 0.2),   # Front-right
        (-0.9, 0.9, 0.2),   # Back-left
        (0.9, 0.9, 0.2)     # Back-right
    ]

    for pos in leg_positions:
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        leg = bpy.context.object
        leg.scale[0] = 0.1  # Width
        leg.scale[1] = 0.1  # Depth
        leg.scale[2] = 0.8  # Height

create_chair()