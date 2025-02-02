import bpy
import bmesh

def create_fabric_triangular_scarf(length, base_width, thickness):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("FabricTriangularScarf")
    obj = bpy.data.objects.new("FabricTriangularScarf", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the bmesh
    bm = bmesh.new()
    
    # Define the vertices of the triangular scarf
    # Adjusting the vertices to create a pronounced triangular shape with a wider base
    v1 = bm.verts.new((-base_width / 2, 0, 0))  # Left base vertex
    v2 = bm.verts.new((base_width / 2, 0, 0))   # Right base vertex
    v3 = bm.verts.new((0, length, 0))             # Tip vertex
    
    # Create additional vertices for the thickness of the scarf
    v4 = bm.verts.new((-base_width / 2, 0, thickness))  # Left top vertex
    v5 = bm.verts.new((base_width / 2, 0, thickness))   # Right top vertex
    v6 = bm.verts.new((0, length, thickness))             # Tip top vertex
    
    # Create faces for the triangular scarf
    bm.faces.new((v1, v2, v3))  # Base triangle
    bm.faces.new((v4, v5, v6))  # Top triangle
    bm.faces.new((v1, v2, v4))  # Side face
    bm.faces.new((v2, v3, v6))  # Side face
    bm.faces.new((v1, v4, v3))  # Side face
    bm.faces.new((v5, v6, v2))  # Side face

    # Smooth the edges using bevel
    bmesh.ops.bevel(bm, geom=bm.verts[:], offset=0.05, segments=5, profile=0.5)

    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the shading to smooth
    bpy.ops.object.shade_smooth()

# Parameters for the fabric triangular scarf
length = 3.0    # Length of the scarf
base_width = 2.5  # Base width of the scarf (wider for better representation)
thickness = 0.3  # Thickness of the scarf for volume

create_fabric_triangular_scarf(length, base_width, thickness)