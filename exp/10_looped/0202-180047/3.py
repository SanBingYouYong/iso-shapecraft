import bpy

def create_shopping_bag():
    # Create the bag body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.6  # Width
    bag.scale[1] = 0.4  # Depth
    bag.scale[2] = 1.2  # Height (increased for more volume)

    # Go to edit mode to modify the shape
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select the top face and scale it to create a tapered effect
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, extend=False)  # Select the top face
    bpy.ops.transform.resize(value=(0.8, 0.8, 1))  # Slightly scale down the top face

    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the handles
    handle_width = 0.2  # Increased width for sturdiness
    handle_length = 0.6  # Increased length for a better representation
    handle_height = 0.3  # Increased height for a robust look

    # Create left handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(-0.45, 0, 1.1))
    left_handle = bpy.context.object
    left_handle.rotation_euler[0] = 1.57  # Rotate to vertical

    # Create right handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_length, location=(0.45, 0, 1.1))
    right_handle = bpy.context.object
    right_handle.rotation_euler[0] = 1.57  # Rotate to vertical

    # Position handles correctly
    left_handle.location.z += handle_height / 2
    right_handle.location.z += handle_height / 2

    # Create a defined base for the bag
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -0.1))
    base = bpy.context.object
    base.scale[0] = 0.65  # Slightly wider than the bag
    base.scale[1] = 0.45  # Slightly deeper than the bag
    base.scale[2] = 0.1   # Thin base for realistic appearance

    # Join the bag and handles and base
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    left_handle.select_set(True)
    right_handle.select_set(True)
    base.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

create_shopping_bag()