import bpy
import bmesh

def create_right_angled_triangle():
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("RightAngledTriangle")
    obj = bpy.data.objects.new("RightAngledTriangle", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh object
    bm = bmesh.new()
    
    # Define vertices for the right-angled triangle
    v1 = bm.verts.new((0, 0, 0))  # Vertex A
    v2 = bm.verts.new((1, 0, 0))  # Vertex B
    v3 = bm.verts.new((0, 1, 0))  # Vertex C
    
    # Create a face from the vertices
    bm.faces.new((v1, v2, v3))
    
    # Finish up, write the bmesh into the mesh
    bm.to_mesh(mesh)
    bm.free()

create_right_angled_triangle()