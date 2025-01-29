import bpy
import bmesh

def create_scalene_triangle(vertices):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("ScaleneTriangle")
    obj = bpy.data.objects.new("ScaleneTriangle", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()
    
    # Create the vertices of the scalene triangle
    v1 = bm.verts.new(vertices[0])
    v2 = bm.verts.new(vertices[1])
    v3 = bm.verts.new(vertices[2])
    
    # Create the face using the vertices
    bm.faces.new((v1, v2, v3))
    
    # Finish up, write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Define vertices for a scalene triangle (no equal sides)
vertices = [(0, 0, 0), (2, 0, 0), (1, 1, 0)]
create_scalene_triangle(vertices)