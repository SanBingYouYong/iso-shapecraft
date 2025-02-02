import bpy
import math

def create_wedge(base_length=2, height=1, taper_length=1):
    # Create a mesh and an object
    mesh = bpy.data.meshes.new(name='Wedge')
    obj = bpy.data.objects.new(name='Wedge', type='MESH')
    
    # Link the object to the collection
    bpy.context.collection.objects.link(obj)
    
    # Define the vertices and faces for the wedge shape
    verts = [
        (0, 0, 0),  # Base point 1
        (base_length, 0, 0),  # Base point 2
        (0, 0, height),  # Top point 1
        (base_length, 0, height),  # Top point 2
        (base_length / 2, taper_length, 0),  # Tapered point at base
        (base_length / 2, taper_length, height)  # Tapered point at top
    ]
    
    faces = [
        (0, 1, 3, 2),  # Side face
        (0, 1, 4),    # Base face
        (2, 3, 5),    # Top face
        (0, 2, 5, 4), # Side face
        (1, 3, 5, 4)  # Side face
    ]
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    # Assign the mesh to the object
    obj.data = mesh

create_wedge()