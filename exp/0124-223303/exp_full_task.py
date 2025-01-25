import bpy

def create_chair():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create chair legs
    leg_height = 1.0
    leg_radius = 0.05
    leg_offset = 0.4

    for x in [-leg_offset, leg_offset]:
        for y in [-leg_offset, leg_offset]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=leg_radius, depth=leg_height, location=(x, y, leg_height / 2)
            )

    # Create seat
    seat_width = leg_offset * 2
    seat_depth = leg_offset * 2
    seat_thickness = 0.1
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(0, 0, leg_height + seat_thickness / 2)
    )
    bpy.ops.transform.resize(value=(seat_width, seat_depth, seat_thickness))

    # Create backrest
    backrest_width = seat_width
    backrest_height = 0.5
    backrest_thickness = 0.05
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=(0, -leg_offset, leg_height + seat_thickness + backrest_height / 2)
    )
    bpy.ops.transform.resize(value=(backrest_width, backrest_thickness, backrest_height))
    
    # Apply smooth shading
    for obj in bpy.context.selected_objects:
        bpy.ops.object.shade_smooth()

create_chair()