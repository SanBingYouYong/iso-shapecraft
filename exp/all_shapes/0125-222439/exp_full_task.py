import bpy

def create_concentric_spheres():
    radii = [2, 4, 6]
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue

    for i, radius in enumerate(radii):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.active_object
        mat = bpy.data.materials.new(name=f"Material_{i}")
        mat.diffuse_color = colors[i]
        mat.use_nodes = False  # Use simple diffuse shader
        sphere.data.materials.append(mat)

create_concentric_spheres()