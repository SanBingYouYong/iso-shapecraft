import bpy

def create_rugby_ball():
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, 0, 0))
    rugby_ball = bpy.context.object
    rugby_ball.scale[0] = 0.5  # Scale along the X-axis
    rugby_ball.scale[1] = 1.0  # Scale along the Y-axis
    rugby_ball.scale[2] = 0.5  # Scale along the Z-axis

create_rugby_ball()