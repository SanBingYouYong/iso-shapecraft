import bpy
import bmesh

def create_shopping_bag():
    # Create the main body of the bag
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.2  # Depth
    bag.scale[2] = 0.8  # Height

    # Create handles
    handle_width = 0.05
    handle_height = 0.4
    handle_depth = 0.2

    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_height, location=(0.5, 0, 0.4))
    handle1 = bpy.context.object
    handle1.rotation_euler[0] = 1.5708  # Rotate to vertical

    bpy.ops.mesh.primitive_cylinder_add(radius=handle_width, depth=handle_height, location=(-0.5, 0, 0.4))
    handle2 = bpy.context.object
    handle2.rotation_euler[0] = 1.5708  # Rotate to vertical

    # Join the bag and handles
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    handle1.select_set(True)
    handle2.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

    # Rename the object
    bpy.context.object.name = "Shopping_Bag"

create_shopping_bag()