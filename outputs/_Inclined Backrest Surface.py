import bpy
import bmesh
from math import radians, pi

def create_inclined_backrest_surface():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create a new mesh and object
    mesh = bpy.data.meshes.new("InclinedBackrest")
    obj = bpy.data.objects.new("InclinedBackrest", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to define the geometry
    bm = bmesh.new()

    # Define vertices for the backrest surface
    bottom_width = 2.0
    height = 1.5
    incline_angle = radians(12.5)  # Average of 10 to 15 degrees
    top_width = bottom_width * 0.8  # Slightly narrower at the top for ergonomic curve

    v1 = bm.verts.new((0, 0, 0))
    v2 = bm.verts.new((bottom_width, 0, 0))
    v3 = bm.verts.new((top_width, 0, height * 0.5))
    v4 = bm.verts.new((0, 0, height))
    v5 = bm.verts.new((bottom_width, 0, height))
    
    # Create the faces of the backrest
    bm.faces.new((v1, v2, v5, v4))  # Back face
    bm.faces.new((v4, v5, v3, v2))  # Top face
    bm.faces.new((v1, v4, v3, v2))  # Side face

    # Smooth the top edge
    for v in (v3, v4):
        v.co.z += 0.2 * (1 - (v.co.x / bottom_width))  # Create a smooth curve upwards

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set shading to smooth
    bpy.ops.object.shade_smooth()

# Call the function to create the inclined backrest surface
create_inclined_backrest_surface()