import bpy

def create_rubber_ball():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
    ball = bpy.context.object
    mat = bpy.data.materials.new(name="RubberMaterial")
    mat.diffuse_color = (0.1, 0.1, 0.1, 1)  # Dark color for rubber
    ball.data.materials.append(mat)

create_rubber_ball()