import bpy
import bmesh
from math import radians, sin, cos

def create_crescent(radius_outer, radius_inner, height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("CrescentMesh")
    obj = bpy.data.objects.new("Crescent", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to work with
    bm = bmesh.new()

    # Create outer half-cylinder
    bmesh.ops.create_circle(bm, cap_tris=True, radius=radius_outer, segments=32, location=(0, 0, 0))
    bmesh.ops.transform(bm, matrix=bpy.Matrix.Translation((0, 0, height / 2)), verts=bm.verts)

    # Create inner half-cylinder
    inner_circle = bmesh.ops.create_circle(bm, cap_tris=True, radius=radius_inner, segments=32, location=(0, 0, 0))
    bmesh.ops.transform(bm, matrix=bpy.Matrix.Translation((0, 0, height / 2)), verts=inner_circle['verts'])

    # Create the crescent shape by removing the inner circle
    bmesh.ops.delete(bm, geom=inner_circle['verts'], context='VERTS')

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the crescent
create_crescent(radius_outer=1, radius_inner=0.5, height=2)