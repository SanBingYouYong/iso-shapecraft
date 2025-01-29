import bpy
import bmesh

def create_diamond():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Diamond")
    obj = bpy.data.objects.new("Diamond", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to define the shape
    bm = bmesh.new()

    # Define vertices for the diamond shape
    verts = [
        bm.verts.new((0, 0, 1)),   # Top vertex
        bm.verts.new((-1, 0, 0)),  # Bottom-left vertex
        bm.verts.new((1, 0, 0)),   # Bottom-right vertex
        bm.verts.new((0, -1, 0)),  # Left vertex
        bm.verts.new((0, 1, 0)),   # Right vertex
        bm.verts.new((0, 0, -1)),  # Bottom vertex
    ]
    
    # Create faces to form the diamond shape
    bmesh.ops.create_face(bm, verts=[verts[0], verts[1], verts[3]])
    bmesh.ops.create_face(bm, verts=[verts[0], verts[3], verts[4]])
    bmesh.ops.create_face(bm, verts=[verts[0], verts[4], verts[2]])
    bmesh.ops.create_face(bm, verts=[verts[0], verts[2], verts[1]])
    bmesh.ops.create_face(bm, verts=[verts[5], verts[1], verts[2]])
    bmesh.ops.create_face(bm, verts=[verts[5], verts[2], verts[4]])
    bmesh.ops.create_face(bm, verts=[verts[5], verts[4], verts[3]])
    bmesh.ops.create_face(bm, verts=[verts[5], verts[3], verts[1]])

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

create_diamond()