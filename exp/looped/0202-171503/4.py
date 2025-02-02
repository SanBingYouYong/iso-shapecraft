import bpy

def create_chair():
    # Clear existing objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the cushioned seat with beveled edges
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.5))
    seat = bpy.context.object
    seat.scale[0] = 1.2  # Width
    seat.scale[1] = 1.2  # Depth
    seat.scale[2] = 0.3  # Height
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.bevel(offset=0.1, segments=10)  # Add bevel for cushioning effect
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the angled backrest
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.7, 1.0))
    backrest = bpy.context.object
    backrest.scale[0] = 1.2  # Width
    backrest.scale[1] = 0.1  # Depth
    backrest.scale[2] = 0.6  # Height
    backrest.rotation_euler[0] = 0.2  # Adjusted tilt for ergonomic position

    # Create the legs with wider and more stable dimensions
    leg_radius = 0.15  # Increased radius for stability
    leg_height = 0.8
    leg_positions = [
        (-0.9, -0.9, leg_height / 2),  # Front-left
        (0.9, -0.9, leg_height / 2),   # Front-right
        (-0.9, 0.9, leg_height / 2),   # Back-left
        (0.9, 0.9, leg_height / 2)     # Back-right
    ]

    for pos in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(radius=leg_radius, depth=leg_height, location=pos)

create_chair()