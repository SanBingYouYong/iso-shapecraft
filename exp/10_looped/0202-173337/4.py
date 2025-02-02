import bpy

def create_shopping_bag():
    # Create the main body of the bag with a rectangular shape
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.25  # Depth
    bag.scale[2] = 0.75  # Height

    # Apply sharp edges using a bevel modifier
    bpy.ops.object.modifier_add(type='BEVEL')
    bag.modifiers["Bevel"].width = 0.02
    bag.modifiers["Bevel"].segments = 4

    # Apply smooth shading
    bpy.ops.object.shade_smooth()

    # Create sturdy handles using cubes for better definition
    handle_width = 0.12
    handle_length = 0.55
    handle_thickness = 0.03

    # Create the first handle
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.2, 0, 0.85))
    handle1 = bpy.context.object
    handle1.scale[0] = handle_length  # Length
    handle1.scale[1] = handle_thickness  # Width
    handle1.scale[2] = handle_width  # Height
    handle1.rotation_euler[0] = 1.5708  # Rotate to horizontal

    # Create the second handle
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.2, 0, 0.85))
    handle2 = bpy.context.object
    handle2.scale[0] = handle_length  # Length
    handle2.scale[1] = handle_thickness  # Width
    handle2.scale[2] = handle_width  # Height
    handle2.rotation_euler[0] = 1.5708  # Rotate to horizontal

    # Join handles with the main bag
    bpy.ops.object.select_all(action='DESELECT')
    bag.select_set(True)
    handle1.select_set(True)
    handle2.select_set(True)
    bpy.context.view_layer.objects.active = bag
    bpy.ops.object.join()

    # Rename the object
    bpy.context.object.name = "Shopping_Bag"

    # Add a material to represent shopping bag texture
    mat = bpy.data.materials.new(name="BagMaterial")
    mat.diffuse_color = (0.8, 0.7, 0.5, 1)  # Light brown color for a paper-like appearance
    bag.data.materials.append(mat)

create_shopping_bag()