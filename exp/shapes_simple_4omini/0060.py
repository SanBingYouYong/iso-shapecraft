import bpy
import bmesh

def create_rounded_square(size=2, radius=0.5, location=(0, 0, 0)):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("RoundedSquare")
    obj = bpy.data.objects.new("RoundedSquare", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh object to create geometry
    bm = bmesh.new()

    # Create the rounded square shape
    bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, segments=16)
    
    # Create the square base
    square_verts = [
        (-size/2, -size/2, 0),
        (size/2, -size/2, 0),
        (size/2, size/2, 0),
        (-size/2, size/2, 0)
    ]
    
    # Create the square face
    square_face = bm.faces.new([bm.verts.new(v) for v in square_verts])
    
    # Create the rounded corners
    for vert in square_face.verts:
        bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, segments=16, cap_tris=True, location=vert.co)

    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the location of the object
    obj.location = location

create_rounded_square()