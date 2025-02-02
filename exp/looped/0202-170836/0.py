import bpy
import bmesh

def create_wedge(length, width, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Wedge")
    obj = bpy.data.objects.new("Wedge", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the vertices
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((length, 0, 0))
    v3 = bm.verts.new((length, width, 0))
    v4 = bm.verts.new((0, width, 0))
    v5 = bm.verts.new((0, width / 2, height))
    
    # Ensure the vertices are updated
    bm.verts.ensure_lookup_table()

    # Create the faces
    bm.faces.new((v1, v2, v3, v4))  # Base face
    bm.faces.new((v1, v2, v5))      # Side face 1
    bm.faces.new((v2, v3, v5))      # Side face 2
    bm.faces.new((v3, v4, v5))      # Side face 3
    bm.faces.new((v4, v1, v5))      # Side face 4

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the wedge shape
create_wedge(length=2, width=1, height=1)