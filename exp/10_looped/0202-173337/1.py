import bpy
import bmesh

def create_shopping_bag():
    # Create the main body of the bag with a rectangular base
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.6  # Width
    bag.scale[1] = 0.3  # Depth
    bag.scale[2] = 0.8  # Height

    # Add some depth and curvature for realism
    bpy.ops.object.modifier_add(type='SUBSURF')
    bag.modifiers["Subdivision"].levels = 1
    bpy.ops.object.shade_smooth()

    # Create wider, tapered handles
    handle_width = 0.1
    handle_height = 0.5
    handle_depth = 0.02

    # Create the first handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_height, location=(0.35, 0, 0.8))
    handle1 = bpy.context.object
    handle1.rotation_euler[0] = 1.5708  # Rotate to vertical
    handle1.scale[2] = 0.5  # Tapering effect

    # Create the second handle
    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_height, location=(-0.35, 0, 0.8))
    handle2 = bpy.context.object
    handle2.rotation_euler[0] = 1.5708  # Rotate to vertical
    handle2.scale[2] = 0.5  # Tapering effect

    # Merge handles with the main bag
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    handle1.select_set(True)
    handle2.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

    # Rename the object
    bpy.context.object.name = "Shopping_Bag"

create_shopping_bag()