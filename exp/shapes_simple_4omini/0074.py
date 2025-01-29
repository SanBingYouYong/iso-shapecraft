import bpy
import bmesh
import math

def create_oval_footprint(radius_x, radius_y, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new('OvalFootprintMesh')
    obj = bpy.data.objects.new('OvalFootprint', mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to build the geometry
    bm = bmesh.new()
    
    # Create the base of the footprint (oval shape)
    bmesh.ops.create_circle(bm, cap_tris=True, radius=radius_x, segments=32)
    
    # Extrude and scale to create the curved top
    top_verts = [v for v in bm.verts]
    bmesh.ops.extrude_vert_indiv(bm, verts=top_verts)
    
    for v in top_verts:
        v.co.z += height  # Move the new top vertices up
        v.co.x *= (radius_y / radius_x)  # Adjust x to maintain the oval shape
    
    # Update the mesh with the new geometry
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the oval footprint
create_oval_footprint(radius_x=1, radius_y=0.5, height=1)