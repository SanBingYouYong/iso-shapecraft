import bpy

def create_chair():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the cushioned seat
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
    seat = bpy.context.object
    seat.scale[0] = 1.0  # Width
    seat.scale[1] = 1.0  # Depth
    seat.scale[2] = 0.3  # Height
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=0.05, segments=10)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the angled backrest
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.55, 1))
    backrest = bpy.context.object
    backrest.scale[0] = 1.0  # Width
    backrest.scale[1] = 0.1  # Depth
    backrest.scale[2] = 0.6  # Height
    backrest.rotation_euler[0] = 0.2  # Rotate backrest for an ergonomic angle

    # Create the legs with consistent dimensions and positions
    leg_size = 0.1
    leg_height = 0.8
    leg_positions = [
        (-0.85, -0.85, leg_height / 2),  # Front-left
        (0.85, -0.85, leg_height / 2),   # Front-right
        (-0.85, 0.85, leg_height / 2),   # Back-left
        (0.85, 0.85, leg_height / 2)     # Back-right
    ]

    for pos in leg_positions:
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        leg = bpy.context.object
        leg.scale[0] = leg_size  # Consistent width
        leg.scale[1] = leg_size  # Consistent depth
        leg.scale[2] = leg_height / 2  # Half height for proper positioning

create_chair()