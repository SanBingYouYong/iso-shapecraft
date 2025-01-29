import bpy
import math

def create_frustum(base_radius_top, base_radius_bottom, height, location):
    bpy.ops.mesh.primitive_cone_add(
        vertices=32,
        radius1=base_radius_bottom,
        radius2=base_radius_top,
        depth=height,
        location=location
    )
    # Move the cone down half its height to center it at the origin
    bpy.ops.transform.translate(value=(0, 0, -height / 2))

# Parameters: top radius, bottom radius, height, location
create_frustum(base_radius_top=1, base_radius_bottom=2, height=3, location=(0, 0, 0))