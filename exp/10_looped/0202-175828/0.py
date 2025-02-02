import bpy

def create_mouse_pad(length=0.3, width=0.2, thickness=0.01):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("MousePadMesh")
    obj = bpy.data.objects.new("MousePad", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Define the vertices and faces for a rectangle
    verts = [
        (0, 0, 0),          # Bottom left
        (length, 0, 0),     # Bottom right
        (length, width, 0), # Top right
        (0, width, 0),      # Top left
        (0, 0, thickness),  # Bottom left (top face)
        (length, 0, thickness), # Bottom right (top face)
        (length, width, thickness), # Top right (top face)
        (0, width, thickness)  # Top left (top face)
    ]

    faces = [
        (0, 1, 2, 3),   # Bottom face
        (4, 5, 6, 7),   # Top face
        (0, 1, 5, 4),   # Side face 1
        (1, 2, 6, 5),   # Side face 2
        (2, 3, 7, 6),   # Side face 3
        (3, 0, 4, 7)    # Side face 4
    ]

    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Add a texture to the surface
    mat = bpy.data.materials.new(name="MousePadMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs[0].default_value = (0.2, 0.2, 0.2, 1)  # Dark gray color
    bsdf.inputs[7].default_value = 0.5  # Roughness for texture
    obj.data.materials.append(mat)

create_mouse_pad()