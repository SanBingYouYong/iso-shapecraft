import bpy
import bmesh

def create_hexagonal_prism(base_edge_length=5, height=15):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for the hexagonal prism
    bm = bmesh.new()

    # Define the vertices of the hexagonal prism
    angle = (2 * 3.14159) / 6  # 360 degrees divided by 6
    vertices = []
    for i in range(6):
        x = base_edge_length * 0.5 * (1 + (0 if i % 2 == 0 else 1)) * (1 if i < 3 else -1) * (1 if i % 3 == 0 else 0)
        y = base_edge_length * 0.5 * (1 + (0 if i % 2 == 1 else 1)) * (1 if i < 3 else -1) * (1 if i % 3 == 1 else 0)
        z = 0
        vertices.append(bm.verts.new((x, y, z)))
        vertices.append(bm.verts.new((x, y, height)))

    # Create faces for the hexagonal prism
    for i in range(6):
        bm.faces.new((vertices[i], vertices[(i + 1) % 6], vertices[(i + 1) % 6 + 6], vertices[i + 6]))

    # Create the top and bottom faces
    bm.faces.new(vertices[:6])  # Bottom face
    bm.faces.new(vertices[6:])  # Top face

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the hexagonal prism
create_hexagonal_prism()