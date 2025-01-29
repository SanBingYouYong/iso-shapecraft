import bpy
import bmesh
from mathutils import Vector

def create_trapezoid(base1_length, base2_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new('Trapezoid')
    obj = bpy.data.objects.new('Trapezoid', mesh)
    
    # Link the object to the collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to build the trapezoid geometry
    bm = bmesh.new()
    
    # Define the vertices of the trapezoid
    v1 = bm.verts.new(Vector((0, 0, 0)))                       # Bottom-left
    v2 = bm.verts.new(Vector((base1_length, 0, 0)))          # Bottom-right
    v3 = bm.verts.new(Vector((base2_length / 2, height, 0))) # Top-right
    v4 = bm.verts.new(Vector((base2_length / 2 - base1_length / 2, height, 0))) # Top-left
    
    # Create the faces
    bm.faces.new((v1, v2, v3, v4))
    
    # Finish up, write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the trapezoid: base1_length, base2_length, height
create_trapezoid(2, 1, 1)
