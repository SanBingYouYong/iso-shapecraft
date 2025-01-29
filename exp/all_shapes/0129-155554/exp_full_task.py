import bpy
import bmesh

def create_square_based_pyramid(base_length=8, height=12, flat_top_height=9):
    # Calculate the coordinates for the pyramid's vertices
    half_base = base_length / 2
    vertices = [
        (-half_base, -half_base, 0),  # Base vertex 1
        (half_base, -half_base, 0),   # Base vertex 2
        (half_base, half_base, 0),    # Base vertex 3
        (-half_base, half_base, 0),   # Base vertex 4
        (0, 0, flat_top_height)        # Apex vertex
    ]
    
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("Pyramid")
    obj = bpy.data.objects.new("Pyramid", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to construct the geometry
    bm = bmesh.new()
    
    # Add vertices
    verts = [bm.verts.new(v) for v in vertices]
    
    # Create faces for the pyramid
    bm.faces.new((verts[0], verts[1], verts[4]))  # Base 1
    bm.faces.new((verts[1], verts[2], verts[4]))  # Base 2
    bm.faces.new((verts[2], verts[3], verts[4]))  # Base 3
    bm.faces.new((verts[3], verts[0], verts[4]))  # Base 4
    bm.faces.new((verts[0], verts[1], verts[2], verts[3]))  # Base face
    
    # Finish the bmesh and write to the mesh
    bm.to_mesh(mesh)
    bm.free()

create_square_based_pyramid()