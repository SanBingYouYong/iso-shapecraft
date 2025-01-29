import bpy
import bmesh
from math import radians

def create_equilateral_triangle():
    # Define the vertices of an equilateral triangle
    size = 2  # Length of each side
    height = (size * (3**0.5)) / 2
    vertices = [
        (0, 0, 0),  # Vertex A
        (size, 0, 0),  # Vertex B
        (size / 2, height, 0)  # Vertex C
    ]
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("EquilateralTriangle")
    obj = bpy.data.objects.new("EquilateralTriangle", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the mesh from the vertices
    bm = bmesh.new()
    for v in vertices:
        bm.verts.new(v)
    
    bm.verts.ensure_lookup_table()
    bm.faces.new(bm.verts)
    
    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_equilateral_triangle()