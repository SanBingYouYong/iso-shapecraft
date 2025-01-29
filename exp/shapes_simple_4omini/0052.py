import bpy
import bmesh
from math import radians

def create_leaf_shape():
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("LeafMesh")
    obj = bpy.data.objects.new("Leaf", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh to construct the leaf shape
    bm = bmesh.new()
    
    # Define the leaf shape vertices
    verts = [
        (0, 0, 0),    # Base of the leaf
        (1, 0.5, 0),  # Right side of the leaf
        (0.5, 1, 0),  # Tip of the leaf
        (0, 0.5, 0),  # Left side of the leaf
    ]
    
    # Create the vertices in bmesh
    vert_list = [bm.verts.new(v) for v in verts]
    
    # Create faces for the leaf shape
    bm.faces.new((vert_list[0], vert_list[1], vert_list[2], vert_list[3]))
    
    # Update the mesh with bmesh data
    bm.to_mesh(mesh)
    bm.free()
    
    # Smooth shading
    bpy.ops.object.shade_smooth()
    
    # Add a material to the leaf
    mat = bpy.data.materials.new(name="LeafMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs['Base Color'].default_value = (0.1, 0.8, 0.1, 1)  # Green color
    obj.data.materials.append(mat)

create_leaf_shape()