import bpy
import bmesh
from mathutils import Vector

def create_pebble_shape(location=(0, 0, 0), scale=(1, 1, 0.5), segments=32):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Pebble")
    obj = bpy.data.objects.new("Pebble", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh for the pebble shape
    bm = bmesh.new()
    
    # Create the base shape using a UV sphere
    bmesh.ops.create_icosphere(bm, subdivisions=0, radius=1, cap_tris=True)
    
    # Scale the shape to create a pebble-like contour
    for v in bm.verts:
        v.co.x *= scale[0]
        v.co.y *= scale[1]
        v.co.z *= scale[2]
    
    # Update the mesh with the bmesh data
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the location of the object
    obj.location = Vector(location)

create_pebble_shape(location=(0, 0, 0), scale=(1.5, 1.0, 0.5))