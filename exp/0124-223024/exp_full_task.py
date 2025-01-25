import bpy
import bmesh

def create_backrest():
    # Set dimensions
    width = 0.5
    depth = 0.1
    height = 0.6
    incline_angle = 15  # degrees

    # Create a new mesh
    mesh = bpy.data.meshes.new("Backrest")
    obj = bpy.data.objects.new("Backrest", mesh)

    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define vertices for a rectangular prism with an incline
    v1 = bm.verts.new((0, -depth/2, 0))  # Bottom left
    v2 = bm.verts.new((width, -depth/2, 0))  # Bottom right
    v3 = bm.verts.new((width, depth/2, 0))  # Top right
    v4 = bm.verts.new((0, depth/2, 0))  # Top left
    v5 = bm.verts.new((0, -depth/2, height))  # Bottom left back
    v6 = bm.verts.new((width, -depth/2, height))  # Bottom right back
    v7 = bm.verts.new((width, depth/2, height))  # Top right back
    v8 = bm.verts.new((0, depth/2, height))  # Top left back

    # Create faces
    bm.faces.new((v1, v2, v3, v4))  # Front face
    bm.faces.new((v5, v6, v7, v8))  # Back face
    bm.faces.new((v1, v2, v6, v5))  # Bottom face
    bm.faces.new((v3, v4, v8, v7))  # Top face
    bm.faces.new((v1, v4, v8, v5))  # Left face
    bm.faces.new((v2, v3, v7, v6))  # Right face

    # Apply incline
    for vert in bm.verts:
        vert.co.z += (vert.co.x / width) * (height * (incline_angle / 90))

    # Create the mesh from the bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the origin to the bottom center of the backrest
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

create_backrest()