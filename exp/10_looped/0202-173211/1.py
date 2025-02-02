import bpy
import bmesh
from mathutils import Vector

def create_triangular_scarf(length=5, width=0.5, thickness=0.1, bevel_amount=0.1):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("TriangularScarf")
    obj = bpy.data.objects.new("TriangularScarf", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh and define the vertices of the triangular shape
    bm = bmesh.new()
    
    # Define the vertices of the triangle
    v1 = bm.verts.new(Vector((0, 0, 0)))          # Base left
    v2 = bm.verts.new(Vector((length, 0, 0)))     # Base right
    v3 = bm.verts.new(Vector((length / 2, width, 0)))  # Peak
    
    # Create the triangle face
    face = bm.faces.new((v1, v2, v3))
    
    # Create the thickness by extruding the triangle
    bmesh.ops.extrude_face_region(bm, geom=[face])
    for v in bm.verts:
        v.co.z += thickness
    
    # Bevel the edges to create a softer look
    bmesh.ops.bevel(bm, geom=face.verts, offset=bevel_amount, segments=8)
    
    # Finish up and write the mesh to the object
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the object mode to 'OBJECT'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

create_triangular_scarf()