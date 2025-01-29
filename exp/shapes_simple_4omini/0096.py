import bpy
import bmesh

def create_sideways_hourglass():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Hourglass")
    obj = bpy.data.objects.new("Hourglass", mesh)
    
    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to construct the geometry
    bm = bmesh.new()

    # Define the vertices for the sideways hourglass
    verts = [
        bm.verts.new((0, 1, 0)),  # Top vertex
        bm.verts.new((1, 0, 0)),  # Middle right vertex
        bm.verts.new((0, -1, 0)), # Bottom vertex
        bm.verts.new((-1, 0, 0)), # Middle left vertex
    ]

    # Create faces for the hourglass shape
    bm.faces.new((verts[0], verts[1], verts[2]))
    bm.faces.new((verts[0], verts[2], verts[3]))
    bm.faces.new((verts[1], verts[0], verts[3]))
    bm.faces.new((verts[1], verts[3], verts[2]))

    # Finish the bmesh and write to mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set the object's location
    obj.location = (0, 0, 0)

create_sideways_hourglass()