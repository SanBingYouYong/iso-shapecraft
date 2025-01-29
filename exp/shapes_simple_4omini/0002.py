import bpy
import bmesh

def create_triangle():
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Triangle")
    obj = bpy.data.objects.new("Triangle", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the triangle
    bm = bmesh.new()
    
    # Define the three vertices of the triangle
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((1, 0, 0))
    v3 = bm.verts.new((0.5, 1, 0))
    
    # Create a face from the vertices
    bm.faces.new((v1, v2, v3))
    
    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_triangle()