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
            bpy.ops.mesh.primitive_cylinder_add(radius=leg_radius, depth=leg_height, location=(x, y, leg_height / 2))
    
    # Create seat
    seat_width = 0.8
    seat_depth = 0.8
    seat_height = 0.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, leg_height + seat_height / 2))
    seat = bpy.context.object
    seat.scale = (seat_width / 2, seat_depth / 2, seat_height / 2)

    # Create backrest
    backrest_width = seat_width
    backrest_height = 0.5
    backrest_thickness = 0.1
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -seat_depth / 2 - backrest_thickness / 2, leg_height + seat_height + backrest_height / 2))
    backrest = bpy.context.object
    backrest.scale = (backrest_width / 2, backrest_thickness / 2, backrest_height / 2)
    
    # Adjust backrest position for curvature
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    backrest.data.vertices[0].co.z += 0.1  # Slightly raise the top vertex for curvature
    backrest.data.vertices[1].co.z += 0.1
    backrest.data.vertices[2].co.z -= 0.1
    backrest.data.vertices[3].co.z -= 0.1
    bpy.ops.object.mode_set(mode='OBJECT')

create_chair()