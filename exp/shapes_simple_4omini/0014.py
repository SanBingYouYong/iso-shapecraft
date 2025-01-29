import bpy
import bmesh

def create_pentagon(size=1):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Pentagon")
    obj = bpy.data.objects.new("Pentagon", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the pentagon geometry
    bm = bmesh.new()
    
    # Define the vertices of the pentagon
    vertices = [
        (size * 0, size, 0),  # Top vertex
        (size * 0.951, size * 0.309, 0),  # Top right vertex
        (size * 0.588, size * -0.809, 0),  # Bottom right vertex
        (size * -0.588, size * -0.809, 0),  # Bottom left vertex
        (size * -0.951, size * 0.309, 0)   # Top left vertex
    ]
    
    # Create the vertices in the bmesh
    verts = [bm.verts.new(v) for v in vertices]

    # Create the pentagon face
    bm.faces.new(verts)

    # Update the mesh with the bmesh data
    bm.to_mesh(mesh)
    bm.free()

create_pentagon()