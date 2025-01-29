import bpy
import bmesh

def create_tetrahedron():
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Tetrahedron")
    obj = bpy.data.objects.new("Tetrahedron", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define vertices for the tetrahedron
    v1 = bm.verts.new((1, 1, 1))
    v2 = bm.verts.new((-1, -1, 1))
    v3 = bm.verts.new((-1, 1, -1))
    v4 = bm.verts.new((1, -1, -1))

    # Create faces using the vertices
    bm.faces.new((v1, v2, v3))
    bm.faces.new((v1, v2, v4))
    bm.faces.new((v1, v3, v4))
    bm.faces.new((v2, v3, v4))

    # Finalize the bmesh and write it to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_tetrahedron()