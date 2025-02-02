import bpy

def create_mouse_pad(length=0.3, width=0.25, height=0.01, texture_path="path_to_texture_image.jpg"):
    # Delete any existing objects to avoid clutter (optional)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height / 2))
    mouse_pad = bpy.context.object
    
    # Scale the plane to the desired dimensions
    mouse_pad.scale[0] = length / 2
    mouse_pad.scale[1] = width / 2
    
    # Reset the rotation and location to ensure it's a flat rectangle
    mouse_pad.rotation_euler = (0, 0, 0)

    # Create a material
    mat = bpy.data.materials.new(name="MousePadMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    # Add texture to the material
    try:
        texture_image = bpy.data.images.load(texture_path)  # Load the texture image
        texture_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
        texture_node.image = texture_image
        
        # Set texture mapping coordinates
        texture_mapping = mat.node_tree.nodes.new('ShaderNodeMapping')
        texture_coord = mat.node_tree.nodes.new('ShaderNodeTexCoord')
        
        # Connect nodes for proper texture mapping
        mat.node_tree.links.new(texture_coord.outputs['UV'], texture_mapping.inputs['Value'])
        mat.node_tree.links.new(texture_mapping.outputs['Vector'], texture_node.inputs['Vector'])
        mat.node_tree.links.new(bsdf.inputs['Base Color'], texture_node.outputs['Color'])
    except Exception as e:
        print(f"Error loading texture image: {e}")
    
    # Assign the material to the mouse pad
    if mouse_pad.data.materials:
        mouse_pad.data.materials[0] = mat
    else:
        mouse_pad.data.materials.append(mat)

create_mouse_pad(texture_path="path_to_texture_image.jpg")  # Update with your actual texture path