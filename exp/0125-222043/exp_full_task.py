import bpy

def create_concentric_spheres():
    # Define the radii and colors for the spheres
    radii = [2, 4, 6]
    colors = [(0.8, 0.1, 0.1, 1), (0.1, 0.8, 0.1, 1), (0.1, 0.1, 0.8, 1)]  # Red, Green, Blue
    
    for i, radius in enumerate(radii):
        # Create a new sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.active_object
        
        # Create a new material
        material = bpy.data.materials.new(name=f"Material_{i}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        
        # Set the base color for the material
        bsdf.inputs['Base Color'].default_value = colors[i]
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        
        # Assign the material to the sphere
        if sphere.data.materials:
            sphere.data.materials[0] = material
        else:
            sphere.data.materials.append(material)

create_concentric_spheres()