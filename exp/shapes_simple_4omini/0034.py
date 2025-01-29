import bpy
import bmesh
from mathutils import Vector

def create_isosceles_triangle(base_length, height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("IsoscelesTriangle")
    obj = bpy.data.objects.new("IsoscelesTriangle", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to work with
    bm = bmesh.new()

    # Define the vertices of the isosceles triangle
    v1 = bm.verts.new((0, 0, 0))  # Bottom left
    v2 = bm.verts.new((base_length, 0, 0))  # Bottom right
    v3 = bm.verts.new((base_length / 2, height, 0))  # Top vertex

    # Create the face using the defined vertices
    bm.faces.new((v1, v2, v3))

    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the isosceles triangle
base_length = 2.0
height = 1.5

create_isosceles_triangle(base_length, height)