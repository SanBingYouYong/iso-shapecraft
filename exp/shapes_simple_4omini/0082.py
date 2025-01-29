import bpy
import bmesh
from math import radians

def create_hourglass():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Hourglass")
    obj = bpy.data.objects.new("HourglassObject", mesh)
    
    # Link object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to work with
    bm = bmesh.new()
    
    # Define the dimensions
    width = 1.0
    height = 2.0
    depth = 1.0

    # Create the top cone
    top_verts = [bm.verts.new((width, 0, height)), bm.verts.new((-width, 0, height)), bm.verts.new((0, width, height)), bm.verts.new((0, -width, height))]
    bmesh.ops.bevel(bm, geom=top_verts, offset=0.1)
    
    # Create the bottom cone
    bottom_verts = [bm.verts.new((width, 0, 0)), bm.verts.new((-width, 0, 0)), bm.verts.new((0, width, 0)), bm.verts.new((0, -width, 0))]
    bmesh.ops.bevel(bm, geom=bottom_verts, offset=0.1)
    
    # Connect the top and bottom
    for i in range(len(top_verts)):
        bm.faces.new((top_verts[i], top_verts[(i + 1) % len(top_verts)], bottom_verts[(i + 1) % len(bottom_verts)], bottom_verts[i]))

    # Finish up
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the hourglass shape
create_hourglass()