import bpy

def create_shopping_bag():
    # Create the bag body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.3  # Depth
    bag.scale[2] = 1.0  # Height

    # Go to edit mode to modify the shape
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select the top face and scale it to create a tapered effect
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, extend=False)  # Select the top face
    bpy.ops.transform.resize(value=(0.8, 0.8, 1))  # Slightly scale down the top face

    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the handles
    handle_width = 0.1
    handle_length = 0.5
    handle_height = 0.2

    # Create left handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(-0.4, 0, 0.9))
    left_handle = bpy.context.object
    left_handle.rotation_euler[0] = 1.57  # Rotate to vertical

    # Create right handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(0.4, 0, 0.9))
    right_handle = bpy.context.object
    right_handle.rotation_euler[0] = 1.57  # Rotate to vertical

    # Position handles correctly
    left_handle.location.z += handle_height / 2
    right_handle.location.z += handle_height / 2

    # Join the bag and handles
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    left_handle.select_set(True)
    right_handle.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

create_shopping_bag()