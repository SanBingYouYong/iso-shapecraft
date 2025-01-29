import bpy
import bmesh

def create_ellipse(a, b, z, segments=32):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=1, radius=1, location=(0, 0, z))
    obj = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    for v in bm.verts:
        v.co.x *= a  # Scale x for ellipse
        v.co.y *= b  # Scale y for ellipse

    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

create_ellipse(2, 1, 0)  # Parameters: a=2, b=1, z=0