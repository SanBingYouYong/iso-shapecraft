import bpy
import bmesh

def create_bowtie():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Bowtie")
    obj = bpy.data.objects.new("Bowtie", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to construct the geometry
    bm = bmesh.new()

    # Define the vertices for the bowtie shape
    v1 = bm.verts.new((0, 1, 0))  # Top triangle point
    v2 = bm.verts.new((-1, 0, 0))  # Bottom left triangle point
    v3 = bm.verts.new((1, 0, 0))  # Bottom right triangle point
    v4 = bm.verts.new((0, -1, 0))  # Bottom triangle point
    v5 = bm.verts.new((-1, 0, 0))  # Bottom left triangle point (again)
    v6 = bm.verts.new((1, 0, 0))  # Bottom right triangle point (again)

    # Create the faces for the two triangles
    bm.faces.new((v1, v2, v3))  # Top triangle
    bm.faces.new((v4, v5, v6))  # Bottom triangle

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

create_bowtie()