import bpy
import bmesh

def create_square_based_pyramid(base_length, height, top_height):
    # Create a new mesh and a new object
    mesh = bpy.data.meshes.new("SquareBasedPyramid")
    obj = bpy.data.objects.new("SquareBasedPyramid", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh object
    bm = bmesh.new()

    # Define the vertices
    half_base = base_length / 2
    vertices = [
        (-half_base, -half_base, 0),  # Vertex 0
        (half_base, -half_base, 0),   # Vertex 1
        (half_base, half_base, 0),    # Vertex 2
        (-half_base, half_base, 0),   # Vertex 3
        (0, 0, top_height)             # Vertex 4 (top vertex)
    ]

    # Add vertices to bmesh
    for v in vertices:
        bm.verts.new(v)

    # Ensure the bmesh updates
    bm.verts.ensure_lookup_table()

    # Create faces (base and four triangular sides)
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[2], bm.verts[3]))  # Base face
    bm.faces.new((bm.verts[0], bm.verts[1], bm.verts[4]))  # Side face 1
    bm.faces.new((bm.verts[1], bm.verts[2], bm.verts[4]))  # Side face 2
    bm.faces.new((bm.verts[2], bm.verts[3], bm.verts[4]))  # Side face 3
    bm.faces.new((bm.verts[3], bm.verts[0], bm.verts[4]))  # Side face 4

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Set object properties
    obj.location = (0, 0, height / 2)

# Parameters for the pyramid
base_length = 8
height = 12
top_height = 9

create_square_based_pyramid(base_length, height, top_height)