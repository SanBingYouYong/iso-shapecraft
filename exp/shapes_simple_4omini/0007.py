import bpy
import bmesh

def create_parallelogram(length, width, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Parallelogram")
    obj = bpy.data.objects.new("Parallelogram", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the vertices of the parallelogram
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((length, 0, 0))
    v3 = bm.verts.new((length - width, height, 0))
    v4 = bm.verts.new((-width, height, 0))
    
    # Create faces
    bm.faces.new((v1, v2, v3, v4))

    # Update the mesh with the bmesh data
    bm.to_mesh(mesh)
    bm.free()

    # Set the location of the object
    obj.location = (0, 0, 0)

# Create a parallelogram with specified dimensions
create_parallelogram(length=2, width=1, height=1)