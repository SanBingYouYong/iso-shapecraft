import bpy
import bmesh
from mathutils import Vector

def create_mountain(size=2, height=3, subdivisions=5):
    bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=True)
    obj = bpy.context.object
    bm = bmesh.from_edit_mesh(obj.data)

    # Create a mountain-like shape
    for v in bm.verts:
        v.co.z = height * (1 - (v.co.x**2 + v.co.y**2) / (size**2))
    
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

    # Subdivide the mesh to create steep slopes
    for _ in range(subdivisions):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=1)
        bpy.ops.object.mode_set(mode='OBJECT')

    # Optionally smooth the surface
    bpy.ops.object.shade_smooth()

create_mountain()