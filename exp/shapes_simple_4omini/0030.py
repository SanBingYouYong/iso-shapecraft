import bpy
import bmesh
from math import radians

def create_ellipse(axis_a, axis_b, location=(0, 0, 0), rotation=(0, 0, 0)):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Ellipse")
    obj = bpy.data.objects.new("Ellipse", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the ellipse
    bm = bmesh.new()
    
    # Create the ellipse vertices
    segments = 64  # Number of segments for the ellipse
    for i in range(segments):
        angle = radians(360 / segments * i)
        x = axis_a * bpy.mathutils.cos(angle)
        y = axis_b * bpy.mathutils.sin(angle)
        bmesh.ops.create_circle(bm, cap_tris=True, radius=1, location=(x, y, 0), segments=1)
        
    # Create the mesh from the bmesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the location and rotation of the object
    obj.location = location
    obj.rotation_euler = rotation

# Parameters for the ellipse
axis_a = 2.0  # Length of the semi-major axis
axis_b = 1.0  # Length of the semi-minor axis
create_ellipse(axis_a, axis_b)