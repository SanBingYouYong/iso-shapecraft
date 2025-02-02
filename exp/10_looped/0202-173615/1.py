import bpy

def create_rubber_ball():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
    ball = bpy.context.object
    
    # Adding a subdivision surface modifier for smoothness
    bpy.ops.object.modifier_add(type='SUBSURF')
    ball.modifiers["Subdivision"].levels = 2
    bpy.ops.object.shade_smooth()
    
    # Creating a new material with a glossy finish
    mat = bpy.data.materials.new(name="RubberMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1)  # Lighter color for rubber
    bsdf.inputs['Roughness'].default_value = 0.3  # Adjust for some glossiness
    
    ball.data.materials.append(mat)

create_rubber_ball()