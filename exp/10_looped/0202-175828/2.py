import bpy
import bmesh
from mathutils import Vector

def create_mouse_pad(length=0.3, width=0.2, thickness=0.01, corner_radius=0.02):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("MousePadMesh")
    obj = bpy.data.objects.new("MousePad", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for rounded corners
    bm = bmesh.new()

    # Create the base rectangle with rounded corners
    verts = [
        Vector((corner_radius, 0, 0)),
        Vector((length - corner_radius, 0, 0)),
        Vector((length, corner_radius, 0)),
        Vector((length, width - corner_radius, 0)),
        Vector((length - corner_radius, width, 0)),
        Vector((corner_radius, width, 0)),
        Vector((0, width - corner_radius, 0)),
        Vector((0, corner_radius, 0)),
    ]

    # Create faces for the bottom rectangle
    bottom_faces = [
        (0, 1, 2, 3, 4, 5, 6, 7)
    ]

    # Create the bottom face
    for v in verts:
        v.z = 0  # Bottom face

    # Create the top face vertices
    top_verts = [v.copy() for v in verts]
    for v in top_verts:
        v.z = thickness  # Top face

    # Add the vertices to the bmesh
    for v in verts + top_verts:
        bmesh.ops.create_vert(bm, co=v)

    # Create bottom and top face
    bmesh.ops.face_create(bm, verts=[bm.verts[i] for i in range(len(verts))])  # Bottom face
    bmesh.ops.face_create(bm, verts=[bm.verts[i + len(verts)] for i in range(len(verts))])  # Top face

    # Create side faces
    for i in range(len(verts)):
        bmesh.ops.face_create(bm, verts=[bm.verts[i], bm.verts[(i + 1) % len(verts)], 
                                          bm.verts[(i + 1) % len(verts) + len(verts)], 
                                          bm.verts[i + len(verts)]])

    # Finish and create the mesh
    bm.to_mesh(mesh)
    bm.free()

    # Add a texture to the surface
    mat = bpy.data.materials.new(name="MousePadMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs[0].default_value = (0.2, 0.2, 0.2, 1)  # Dark gray color
    bsdf.inputs[7].default_value = 0.5  # Roughness for texture

    # Adding bump for texture effect
    bump_node = mat.node_tree.nodes.new('ShaderNodeBump')
    bump_node.inputs[0].default_value = 0.1  # Strength of the bump
    texture_node = mat.node_tree.nodes.new('ShaderNodeTexNoise')
    texture_node.inputs[2].default_value = 5.0  # Scale of the noise texture

    # Link nodes
    mat.node_tree.links.new(texture_node.outputs[0], bump_node.inputs[2])
    mat.node_tree.links.new(bump_node.outputs[0], bsdf.inputs[21])  # Normal input for the Principled BSDF

    obj.data.materials.append(mat)

create_mouse_pad()