import bpy
import bmesh

def create_smooth_wedge(length, width, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("SmoothWedge")
    obj = bpy.data.objects.new("SmoothWedge", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define the vertices for a smoother tapered end and pronounced wedge shape
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((length, 0, 0))
    v3 = bm.verts.new((length, width * 0.5, 0))  # Adjusting position for a more pronounced wedge
    v4 = bm.verts.new((0, width, 0))
    
    # Adding additional vertices to smooth the taper
    v5 = bm.verts.new((length * 0.75, width * 0.25, height * 0.5))
    v6 = bm.verts.new((length * 0.75, width * 0.75, height * 0.5))
    v7 = bm.verts.new((length, width * 0.5, height))

    # Ensure the vertices are updated
    bm.verts.ensure_lookup_table()

    # Create the faces
    bm.faces.new((v1, v2, v3, v4))      # Base face
    bm.faces.new((v1, v2, v7))          # Side face 1
    bm.faces.new((v2, v3, v7))          # Side face 2
    bm.faces.new((v3, v6, v7))          # Side face 3
    bm.faces.new((v4, v3, v6))          # Side face 4
    bm.faces.new((v4, v1, v5))          # Side face 5
    bm.faces.new((v5, v6, v4))          # Side face 6

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the smooth wedge shape
create_smooth_wedge(length=2, width=1, height=1)