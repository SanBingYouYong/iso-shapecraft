import bpy
import bmesh

def create_hemisphere(radius, location):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location, segments=32, ring_count=16)
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Remove the bottom half of the sphere
    for v in bm.verts[:]:
        if v.co.z < 0:
            bm.verts.remove(v)
    
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

create_hemisphere(radius=1, location=(0, 0, 0))