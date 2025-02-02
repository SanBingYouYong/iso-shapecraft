import bpy
import bmesh

def create_wedge(length=2.0, width=1.0, height=1.0):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Wedge")
    obj = bpy.data.objects.new("Wedge", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh data
    bm = bmesh.new()

    # Define vertices for a wedge shape
    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((length, 0, 0))
    v3 = bm.verts.new((length, width, 0))
    v4 = bm.verts.new((0, width, 0))
    v5 = bm.verts.new((0, 0, height))
    v6 = bm.verts.new((length, 0, height))
    v7 = bm.verts.new((length, width, height))
    v8 = bm.verts.new((0, width, height))

    # Create faces for the wedge
    bm.faces.new((v1, v2, v3, v4))  # Base face
    bm.faces.new((v1, v2, v6, v5))  # Side face 1
    bm.faces.new((v2, v3, v7, v6))  # Side face 2
    bm.faces.new((v3, v4, v8, v7))  # Side face 3
    bm.faces.new((v4, v1, v5, v8))  # Side face 4
    bm.faces.new((v5, v6, v7, v8))  # Top face

    # Finish the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the origin to the center of the geometry
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_wedge()