import bpy

def create_concentric_spheres():
    radii = [2, 4, 6]
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue

    for i, radius in enumerate(radii):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.object
        sphere.name = f"Sphere_{i+1}"

        # Set the material
        mat = bpy.data.materials.new(name=f"Material_{i+1}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs[0].default_value = colors[i]  # Set color
        bsdf.inputs[7].default_value = 0.1  # Set roughness for matte finish

        if sphere.data.materials:
            sphere.data.materials[0] = mat
        else:
            sphere.data.materials.append(mat)

create_concentric_spheres()