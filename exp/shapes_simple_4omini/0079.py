import bpy
import bmesh

def create_wedge_shape(location=(0, 0, 0), size=2):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new('Wedge')
    obj = bpy.data.objects.new('Wedge', mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the wedge geometry
    bm = bmesh.new()
    
    # Define the vertices of the wedge
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((size, 0, 0))
    v3 = bm.verts.new((size / 2, size, 0))
    v4 = bm.verts.new((0, 0, size))
    
    # Create faces for the wedge
    bm.faces.new((v1, v2, v3))
    bm.faces.new((v1, v2, v4))
    bm.faces.new((v2, v3, v4))
    bm.faces.new((v1, v3, v4))
    
    # Update the mesh with the new geometry
    bm.to_mesh(mesh)
    bm.free()
    
    # Move the object to the specified location
    obj.location = location

create_wedge_shape()