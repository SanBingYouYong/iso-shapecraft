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
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (1.0, 0.5, 0.2, 1)  # Vibrant orange color
    bsdf.inputs['Roughness'].default_value = 0.2  # Adjust for some glossiness
    bsdf.inputs['Specular'].default_value = 0.5  # Add specular highlight

    # Add a noise texture to simulate rubber imperfections
    texture = mat.node_tree.nodes.new('ShaderNodeTexNoise')
    texture.inputs['Scale'].default_value = 5.0  # Adjust scale for the texture
    texture.outputs[0].default_value = 0.5  # Adjust to influence bumpiness

    # Connect texture to the normal input of the BSDF shader
    bump = mat.node_tree.nodes.new('ShaderNodeBump')
    mat.node_tree.links.new(texture.outputs['Fac'], bump.inputs['Height'])
    mat.node_tree.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    # Assign material to the ball
    ball.data.materials.append(mat)

    # Add a reference object (a plane) to give context to the size of the ball
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, -0.5))

create_rubber_ball()