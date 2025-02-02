import bpy
import bmesh

def create_wedge_shape(length, width, height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("WedgeMesh")
    obj = bpy.data.objects.new("Wedge", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh
    bm = bmesh.new()

    # Define the vertices of the wedge shape
    v1 = bm.verts.new((0, 0, 0))                 # Base corner 1
    v2 = bm.verts.new((length, 0, 0))            # Base corner 2
    v3 = bm.verts.new((length, width, 0))        # Base corner 3
    v4 = bm.verts.new((0, width, 0))              # Base corner 4
    v5 = bm.verts.new((length / 2, width / 2, height))  # Tapered end

    # Create faces for the wedge shape
    bm.faces.new((v1, v2, v5))  # Side 1
    bm.faces.new((v2, v3, v5))  # Side 2
    bm.faces.new((v3, v4, v5))  # Side 3
    bm.faces.new((v4, v1, v5))  # Side 4
    bm.faces.new((v1, v2, v3, v4))  # Base

    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the wedge shape
create_wedge_shape(length=2, width=1, height=1)