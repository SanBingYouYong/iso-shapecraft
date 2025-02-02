import bpy

def create_serving_tray(length=1.0, width=0.5, base_height=0.02, side_height=0.1):
    # Create the base of the tray
    bpy.ops.mesh.primitive_plane_add(size=length, location=(0, 0, base_height))
    base = bpy.context.object
    base.name = "ServingTrayBase"
    
    # Create the sides of the tray
    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(length / 2, 0, base_height + side_height / 2))
    side1 = bpy.context.object
    side1.name = "TraySide1"
    side1.scale[0] = length / 2
    side1.scale[1] = 0.025  # Thin side for width
    side1.scale[2] = side_height

    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(-length / 2, 0, base_height + side_height / 2))
    side2 = bpy.context.object
    side2.name = "TraySide2"
    side2.scale[0] = length / 2
    side2.scale[1] = 0.025  # Thin side for width
    side2.scale[2] = side_height

    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, width / 2, base_height + side_height / 2))
    side3 = bpy.context.object
    side3.name = "TraySide3"
    side3.scale[0] = 0.025  # Thin side for length
    side3.scale[1] = width / 2
    side3.scale[2] = side_height

    bpy.ops.mesh.primitive_cube_add(size=side_height, location=(0, -width / 2, base_height + side_height / 2))
    side4 = bpy.context.object
    side4.name = "TraySide4"
    side4.scale[0] = 0.025  # Thin side for length
    side4.scale[1] = width / 2
    side4.scale[2] = side_height

    # Create a new material
    mat = bpy.data.materials.new(name="TrayMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.8, 0.5, 0.3, 1)  # Wood-like color

    # Assign the material to the base
    base.data.materials.append(mat)

    # Add a simple texture to the base of the tray
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.uv.unwrap()  # Unwrap for texture application
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set a random offset for the base vertices to create texture
    for vertex in base.data.vertices:
        vertex.co.z += (0.01 * (0.5 - bpy.utils.random.uniform(0.0, 1.0)))

create_serving_tray()