import bpy
import bmesh

def create_circle(radius=1, location=(0, 0, 0), segments=32):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("Circle")
    obj = bpy.data.objects.new("Circle", mesh)
    
    # Link the object to the current collection
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to hold the geometry
    bm = bmesh.new()
    
    # Create a circle in bmesh
    bmesh.ops.create_circle(bm, cap_tris=True, radius=radius, segments=segments)

    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the location of the object
    obj.location = location

create_circle()