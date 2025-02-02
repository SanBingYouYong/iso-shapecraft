import bpy

def create_shopping_bag():
    # Create the bag body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.3  # Depth
    bag.scale[2] = 1.2  # Height for a taller bag

    # Go to edit mode to modify the shape
    bpy.ops.object.mode_set(mode='EDIT')

    # Select and scale the top face to create a tapered effect
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, extend=False)  # Select the top face
    bpy.ops.transform.resize(value=(0.9, 0.9, 1))  # Slightly scale down the top face for tapering

    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the base for support
    base_height = 0.1  # Height of the base
    base_width = 0.55   # Base width
    base_depth = 0.35   # Base depth

    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, -base_height / 2))
    base = bpy.context.object
    base.scale[0] = base_width  # Width of the base
    base.scale[1] = base_depth   # Depth of the base
    base.scale[2] = base_height   # Height of the base

    # Create the handles using planes to make them flatter
    handle_width = 0.1  # Width of the handles
    handle_length = 0.5  # Length of the handles
    handle_thickness = 0.05  # Thickness to give it some volume

    # Create left handle
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.4, 0, 1.1))
    left_handle = bpy.context.object
    left_handle.scale[0] = handle_length  # Length of the handle
    left_handle.scale[1] = handle_width   # Width of the handle
    left_handle.rotation_euler[0] = 1.57  # Rotate to vertical
    left_handle.location.z += handle_thickness / 2  # Position it correctly

    # Create right handle
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.4, 0, 1.1))
    right_handle = bpy.context.object
    right_handle.scale[0] = handle_length  # Length of the handle
    right_handle.scale[1] = handle_width   # Width of the handle
    right_handle.rotation_euler[0] = 1.57  # Rotate to vertical
    right_handle.location.z += handle_thickness / 2  # Position it correctly

    # Join the bag, base, and handles
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    base.select_set(True)
    left_handle.select_set(True)
    right_handle.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

create_shopping_bag()