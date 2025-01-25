import bpy

def create_concentric_spheres():
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue
    radii = [2, 4, 6]

    for i in range(len(radii)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radii[i], location=(0, 0, 0))
        sphere = bpy.context.object
        material = bpy.data.materials.new(name=f'SphereMaterial{i}')
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get('Principled BSDF')
        bsdf.inputs['Base Color'].default_value = colors[i]
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        sphere.data.materials.append(material)

create_concentric_spheres()