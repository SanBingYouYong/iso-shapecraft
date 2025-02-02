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

    # Define the vertices for a more defined taper and consistent proportions
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((length, 0, 0))
    v3 = bm.verts.new((length, width * 0.5, height * 0.4))  # More defined taper
    v4 = bm.verts.new((0, width, 0))
    
    # Adding more vertices for a smooth taper and to enhance proportions
    v5 = bm.verts.new((length * 0.9, width * 0.2, height))
    v6 = bm.verts.new((length * 0.9, width * 0.8, height))
    v7 = bm.verts.new((length * 0.6, width * 0.5, height * 0.9))  # Adjusted for better angle

    # Ensure the vertices are updated
    bm.verts.ensure_lookup_table()

    # Create the faces without duplicates
    bm.faces.new((v1, v2, v3, v4))      # Base face
    bm.faces.new((v1, v2, v5))          # Side face 1
    bm.faces.new((v2, v3, v5))          # Side face 2
    bm.faces.new((v3, v6, v5))          # Side face 3
    bm.faces.new((v4, v3, v6))          # Side face 4
    bm.faces.new((v4, v1, v7))          # Side face 5
    bm.faces.new((v7, v6, v4))          # Side face 6

    # Make sure to only create unique faces
    try:
        bm.faces.new((v5, v6, v3))      # Adjusted to avoid potential duplicates
    except ValueError:
        pass  # Ignore if the face already exists

    # Recalculate normals for consistent shading
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

    # Set smooth shading for the object
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the smooth wedge shape
create_smooth_wedge(length=2, width=1, height=1)