import bpy

def create_concentric_spheres():
    radii = [2, 4, 6]
    colors = [(0.8, 0.1, 0.1, 1), (0.1, 0.8, 0.1, 1), (0.1, 0.1, 0.8, 1)]
    
    for radius, color in zip(radii, colors):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius)
        sphere = bpy.context.object
        mat = bpy.data.materials.new(name=f"Material_{radius}")
        mat.diffuse_color = color
        sphere.data.materials.append(mat)
        sphere.select_set(True)
        bpy.ops.object.shade_smooth()
        sphere.location = (0, 0, 0)

create_concentric_spheres()