import bpy
import bmesh

def create_checkmark(size=1):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Checkmark")
    obj = bpy.data.objects.new("Checkmark", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define geometry
    bm = bmesh.new()
    
    # Define vertices for the checkmark shape
    v1 = bm.verts.new((0, 0, 0))     # Start point
    v2 = bm.verts.new((0, size, 0))  # Vertical line top
    v3 = bm.verts.new((size, size, 0))  # Horizontal line end
    v4 = bm.verts.new((size, 0, 0))  # Horizontal line start
    
    # Create edges for the checkmark
    bm.edges.new((v1, v2))  # Vertical line
    bm.edges.new((v2, v3))  # Diagonal line
    bm.edges.new((v3, v4))  # Bottom edge
    bm.edges.new((v4, v1))  # Closing the shape
    
    # Finish the bmesh and write to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_checkmark(size=2)