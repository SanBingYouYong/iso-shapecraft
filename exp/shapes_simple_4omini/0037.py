import bpy
import bmesh
from math import radians
import mathutils

def create_knot(radius=1, loops=3, segments=32):
    # Create a new mesh
    mesh = bpy.data.meshes.new("Knot")
    obj = bpy.data.objects.new("Knot", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    
    # Create a BMesh for the knot
    bm = bmesh.new()

    for i in range(loops * segments):
        theta = i * (2 * math.pi / segments)
        phi = (i * (math.pi / 2)) / segments

        x = radius * (1 + math.cos(phi)) * math.cos(theta)
        y = radius * (1 + math.cos(phi)) * math.sin(theta)
        z = radius * math.sin(phi)

        bmesh.ops.create_circle(bm, cap_tris=True, radius=0.1, location=(x, y, z), segments=8)

    # Finish up
    bm.to_mesh(mesh)
    bm.free()
    
    # Set smooth shading
    for face in mesh.polygons:
        face.use_smooth = True

create_knot()