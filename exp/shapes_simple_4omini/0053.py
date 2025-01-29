import bpy
import bmesh
import math

def create_hexagonal_tile(radius=1):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalTile")
    obj = bpy.data.objects.new(mesh.name, mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a BMesh
    bm = bmesh.new()

    # Define the vertices for the hexagon
    for i in range(6):
        angle = math.radians(60 * i)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        z = 0
        bmesh.ops.create_vert(bm, co=(x, y, z))

    # Create the faces for the hexagon
    verts = [v for v in bm.verts]
    bmesh.ops.create_face(bm, verts=verts)

    # Write the bmesh data to the mesh
    bm.to_mesh(mesh)
    bm.free()

# Call the function to create the hexagonal tile
create_hexagonal_tile()