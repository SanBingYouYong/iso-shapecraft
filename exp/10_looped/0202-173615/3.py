import bpy

def create_rubber_ball():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a UV sphere to represent the rubber ball
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
    ball = bpy.context.object
    
    # Adding a subdivision surface modifier for smoothness
    bpy.ops.object.modifier_add(type='SUBSURF')
    ball.modifiers["Subdivision"].levels = 1
    bpy.ops.object.shade_smooth()
    
    # Creating a new material with a glossy finish and some texture
    mat = bpy.data.materials.new(name="RubberMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create Principled BSDF shader
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.inputs['Base Color'].default_value = (1.0, 0.5, 0.2, 1)  # Vibrant orange color
    bsdf.inputs['Roughness'].default_value = 0.2  # Adjust for some glossiness
    bsdf.inputs['Specular'].default_value = 0.5  # Add specular highlight
    
    # Create Noise Texture
    texture = nodes.new('ShaderNodeTexNoise')
    texture.inputs['Scale'].default_value = 5.0  # Adjust scale for the texture
    
    # Create Bump Node
    bump = nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.1  # Adjust strength for bumpiness
    
    # Link the nodes
    links.new(texture.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Create Output Node
    output = nodes.new('ShaderNodeOutputMaterial')
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # Assign material to the ball
    ball.data.materials.append(mat)

    # Add a reference object (a plane) to give context to the size of the ball
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.5))

create_rubber_ball()