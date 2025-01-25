import bpy
import bmesh

def create_hexagonal_prism(base_edge_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh geometry
    bm = bmesh.new()
    
    # Define the vertices of the hexagonal base
    angle = 2 * 3.14159 / 6  # 360 degrees divided by 6 for hexagon
    vertices = [(base_edge_length * 0.5 * (1 + 0.5 * (3**0.5)) * (1 if i % 2 == 0 else -1), 
                 base_edge_length * 0.5 * (3**0.5) * (1 if i % 2 == 0 else -1), 
                 0) for i in range(6)]
    
    # Create top and bottom vertices
    bottom_verts = [bm.verts.new(v) for v in vertices]
    top_verts = [bm.verts.new((v[0], v[1], height)) for v in vertices]

    # Create faces for the bottom and top
    bm.faces.new(bottom_verts)
    bm.faces.new(top_verts)

    # Create side faces
    for i in range(6):
        v1 = bottom_verts[i]
        v2 = bottom_verts[(i + 1) % 6]
        v3 = top_verts[(i + 1) % 6]
        v4 = top_verts[i]
        bm.faces.new((v1, v2, v3, v4))

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the hexagonal prism
create_hexagonal_prism(5, 15)