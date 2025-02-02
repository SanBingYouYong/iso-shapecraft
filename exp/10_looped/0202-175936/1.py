import bpy
import bmesh

def create_narrow_triangular_scarf(length, base_width):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("NarrowTriangularScarf")
    obj = bpy.data.objects.new("NarrowTriangularScarf", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the bmesh
    bm = bmesh.new()
    
    # Define the vertices of the elongated triangular scarf
    # Adjusting the width to make it more narrow towards the tip
    v1 = bm.verts.new((-base_width / 4, 0, 0))  # Left base vertex
    v2 = bm.verts.new((base_width / 4, 0, 0))   # Right base vertex
    v3 = bm.verts.new((0, length, 0))             # Tip vertex
    
    # Create a face from the vertices
    bm.faces.new((v1, v2, v3))
    
    # Update the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set the shading to smooth
    bpy.ops.object.shade_smooth()

# Parameters for the narrow triangular scarf
length = 3.0  # Length of the scarf
base_width = 1.0  # Base width of the scarf

create_narrow_triangular_scarf(length, base_width)