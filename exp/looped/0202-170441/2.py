import bpy
import bmesh

def create_wedge(length, width, height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Wedge")
    obj = bpy.data.objects.new("Wedge", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the shape
    bm = bmesh.new()

    # Define the vertices of the wedge
    v1 = bm.verts.new((0, 0, 0))  # Bottom left
    v2 = bm.verts.new((length, 0, 0))  # Bottom right
    v3 = bm.verts.new((length, width, 0))  # Top right
    v4 = bm.verts.new((0, width, 0))  # Top left
    v5 = bm.verts.new((length * 0.5, width * 0.5, height * 1.2))  # Tapered top with increased height

    # Create the faces of the wedge
    bm.faces.new((v1, v2, v3, v4))  # Bottom face
    bm.faces.new((v1, v2, v5))  # Side face
    bm.faces.new((v2, v3, v5))  # Side face
    bm.faces.new((v3, v4, v5))  # Side face
    bm.faces.new((v4, v1, v5))  # Side face

    # Add a bevel to the top vertex to smooth the taper
    bmesh.ops.bevel(bm, geom=[v5], offset=0.2)

    # Finish up and write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Recalculate normals for smooth shading
    bpy.ops.object.shade_smooth()

create_wedge(2, 1, 0.5)