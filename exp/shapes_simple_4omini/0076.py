import bpy
import bmesh

def create_obtuse_triangle():
    # Define the vertices of the triangle
    verts = [(0, 0, 0), (2, 0, 0), (1, 2, 0)]  # The angle at vertex (2, 0, 0) is obtuse
    edges = []
    faces = [(0, 1, 2)]
    
    # Create a new mesh
    mesh = bpy.data.meshes.new("ObtuseTriangle")
    obj = bpy.data.objects.new("ObtuseTriangle", mesh)
    
    bpy.context.collection.objects.link(obj)
    
    # Create the mesh from the data
    bm = bmesh.new()
    for v in verts:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()
    for f in faces:
        bm.faces.new([bm.verts[i] for i in f])
    
    bm.to_mesh(mesh)
    bm.free()

create_obtuse_triangle()