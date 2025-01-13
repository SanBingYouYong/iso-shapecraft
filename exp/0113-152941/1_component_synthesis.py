import bpy

def create_backrest():
    # Delete default cube
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a rectangle for the backrest
    bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 1.5))
    backrest = bpy.context.active_object
    backrest.name = "Backrest"

    # Scale to create a tall rectangular shape
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.resize(value=(1, 0.1, 1.5))  # width, depth, height
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add a subdivision surface for smooth edges
    bpy.ops.object.modifier_add(type='SUBSURF')
    backrest.modifiers["Subdivision"].levels = 2
    bpy.ops.object.shade_smooth()

    # Add a bevel modifier for rounded edges
    bpy.ops.object.modifier_add(type='BEVEL')
    backrest.modifiers["Bevel"].width = 0.05
    backrest.modifiers["Bevel"].segments = 5

    # Apply all modifiers
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    bpy.ops.object.modifier_apply(modifier="Bevel")

    # Rotate the backrest slightly backward for ergonomic support
    backrest.rotation_euler = (0.1, 0, 0)  # slight backward inclination

create_backrest()