import bpy

def create_shopping_bag():
    # Create the main body of the bag with a rectangular base and upright sides
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.25  # Depth
    bag.scale[2] = 0.7  # Height

    # Add some depth to the bag for realism
    bpy.ops.object.modifier_add(type='SUBSURF')
    bag.modifiers["Subdivision"].levels = 1
    bpy.ops.object.shade_smooth()

    # Create sturdy handles as flat objects
    handle_width = 0.1
    handle_length = 0.4
    handle_thickness = 0.02

    # Create the first handle
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.25, 0, 0.8))
    handle1 = bpy.context.object
    handle1.scale[0] = handle_length  # Length
    handle1.scale[1] = handle_width  # Width
    handle1.scale[2] = handle_thickness  # Thickness
    handle1.rotation_euler[0] = 0.5  # Slight rotation for a better appearance

    # Create the second handle
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.25, 0, 0.8))
    handle2 = bpy.context.object
    handle2.scale[0] = handle_length  # Length
    handle2.scale[1] = handle_width  # Width
    handle2.scale[2] = handle_thickness  # Thickness
    handle2.rotation_euler[0] = 0.5  # Slight rotation for a better appearance

    # Join handles with the main bag
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    handle1.select_set(True)
    handle2.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

    # Rename the object
    bpy.context.object.name = "Shopping_Bag"

create_shopping_bag()