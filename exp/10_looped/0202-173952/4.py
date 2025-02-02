import bpy

def create_shoe_box(length, width, height, bevel_depth):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    # Create the base shape
    bpy.ops.mesh.primitive_cube_add(size=1)
    shoe_box = bpy.context.object
    shoe_box.scale = (length / 2, width / 2, height / 2)
    shoe_box.location = (0, 0, height / 2)

    # Add a bevel modifier for slightly sharper corners
    bevel_modifier = shoe_box.modifiers.new(name="Bevel", type='BEVEL')
    bevel_modifier.width = bevel_depth
    bevel_modifier.segments = 2  # Fewer segments for sharper edges
    bevel_modifier.profile = 0.1  # Slight rounding for a more defined edge

    # Add a material to mimic cardboard texture
    mat = bpy.data.materials.new(name="CardboardMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    # Set a brownish color
    bsdf.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1)  
    bsdf.inputs['Roughness'].default_value = 0.5  # Slightly rough surface

    # Assign the material to the shoe box
    if shoe_box.data.materials:
        shoe_box.data.materials[0] = mat
    else:
        shoe_box.data.materials.append(mat)

create_shoe_box(4, 1.5, 0.6, 0.02)