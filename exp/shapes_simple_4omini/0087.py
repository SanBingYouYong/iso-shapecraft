import bpy
import bmesh

def create_trapezoid(top_length, bottom_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Trapezoid")
    obj = bpy.data.objects.new("Trapezoid", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to construct the trapezoid
    bm = bmesh.new()

    # Define the vertices of the trapezoid
    top_half = top_length / 2
    bottom_half = bottom_length / 2
    
    v1 = bm.verts.new((-top_half, 0, 0))
    v2 = bm.verts.new((top_half, 0, 0))
    v3 = bm.verts.new((-bottom_half, height, 0))
    v4 = bm.verts.new((bottom_half, height, 0))
    
    # Create faces
    bm.faces.new((v1, v2, v4, v3))

    # Finish up, write the bmesh into the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the trapezoid
top_length = 2.0
bottom_length = 4.0
height = 2.0

create_trapezoid(top_length, bottom_length, height)