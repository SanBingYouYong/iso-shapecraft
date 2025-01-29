import bpy

def create_fish_shape():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the body of the fish
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    fish_body = bpy.context.object
    fish_body.name = "FishBody"

    # Scale the body to make it more fish-like
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.transform.resize(value=(1.5, 0.5, 0.5))
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the tail of the fish
    bpy.ops.mesh.primitive_cone_add(radius1=0, radius2=0.5, depth=1, location=(1.5, 0, 0))
    fish_tail = bpy.context.object
    fish_tail.name = "FishTail"

    # Rotate the tail to point it backwards
    fish_tail.rotation_euler[1] = 3.14159  # Rotate 180 degrees along the Y axis

    # Join the body and the tail into a single object
    bpy.ops.object.select_all(action='DESELECT')
    fish_body.select_set(True)
    fish_tail.select_set(True)
    bpy.context.view_layer.objects.active = fish_body
    bpy.ops.object.join()

    # Set origin to geometry
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_fish_shape()