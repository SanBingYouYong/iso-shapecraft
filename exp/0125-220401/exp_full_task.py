import bpy
import bmesh

def create_hexagonal_prism(base_edge_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the bmesh for the hexagonal prism
    bm = bmesh.new()
    
    # Define the vertices for a hexagon
    vertices = []
    for i in range(6):
        angle = i * (3.14159 / 3)  # 60 degrees in radians
        x = base_edge_length * 0.5 * (1 + (1 if i % 2 == 0 else -1)) * (3**0.5)  # Hexagon width
        y = base_edge_length * 0.5 * (1 if i % 2 == 0 else -1)
        vertices.append(bm.verts.new((x, y, 0)))
    
    # Create the top and bottom faces of the prism
    bottom_face = bm.faces.new(vertices)
    top_face = bm.faces.new([bm.verts.new((v.co.x, v.co.y, height)) for v in vertices])
    
    # Connect the top and bottom faces
    for i in range(6):
        bm.faces.new((vertices[i], vertices[(i + 1) % 6], top_face.verts[(i + 1) % 6], top_face.verts[i]))
    
    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()

create_hexagonal_prism(5, 15)