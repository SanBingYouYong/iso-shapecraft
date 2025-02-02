import bpy
import bmesh
from mathutils import Vector

def create_triangular_scarf(length=5, base_width=0.5, tip_width=0.2, thickness=0.1, bevel_amount=0.1):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("TriangularScarf")
    obj = bpy.data.objects.new("TriangularScarf", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh and define the vertices of the triangular shape
    bm = bmesh.new()
    
    # Define the vertices of the triangle
    v1 = bm.verts.new(Vector((0, 0, 0)))            # Base left
    v2 = bm.verts.new(Vector((length, 0, 0)))       # Base right
    v3 = bm.verts.new(Vector((length / 2, base_width, 0)))  # Base peak
    
    # Create the tapered tip of the scarf
    v4 = bm.verts.new(Vector((length - 1, tip_width, 0)))  # Tip right
    v5 = bm.verts.new(Vector((1, tip_width, 0)))            # Tip left
    
    # Create the triangle faces for the scarf
    bm.faces.new((v1, v2, v3))  # Base face
    bm.faces.new((v3, v4, v5))  # Right tip face
    bm.faces.new((v3, v5, v1))   # Left tip face
    
    # Create the thickness by extruding the triangle
    bmesh.ops.extrude_face_region(bm, geom=[f for f in bm.faces])
    for v in bm.verts:
        v.co.z += thickness
    
    # Bevel the edges to create a softer look
    bmesh.ops.bevel(bm, geom=[v1, v2, v3, v4, v5], offset=bevel_amount, segments=8)
    
    # Finish up and write the mesh to the object
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the object mode to 'OBJECT'
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT')

    # Add material for realism
    mat = bpy.data.materials.new(name="ScarfMaterial")
    mat.diffuse_color = (0.8, 0.2, 0.2, 1)  # Example color (red-ish)
    obj.data.materials.append(mat)

create_triangular_scarf()