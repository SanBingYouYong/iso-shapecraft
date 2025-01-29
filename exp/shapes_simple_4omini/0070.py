import bpy
import bmesh

def create_trapezoid(top_width, bottom_width, height):
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Trapezoid")
    obj = bpy.data.objects.new("Trapezoid", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a BMesh
    bm = bmesh.new()
    
    # Define the vertices for the trapezoid
    v1 = bm.verts.new((top_width / 2, 0, height))
    v2 = bm.verts.new((-top_width / 2, 0, height))
    v3 = bm.verts.new((bottom_width / 2, 0, 0))
    v4 = bm.verts.new((-bottom_width / 2, 0, 0))
    
    # Create the faces of the trapezoid
    bm.faces.new((v1, v2, v4, v3))  # Top face
    bm.faces.new((v1, v2, v2))      # Side faces
    bm.faces.new((v3, v4, v1, v2))  # Bottom face
    
    # Write the bmesh to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Create a trapezoid with specified dimensions
create_trapezoid(top_width=2, bottom_width=1, height=1)