import bpy
import bmesh

def create_mouse_pad(length=0.3, width=0.2, thickness=0.01, corner_radius=0.02):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("MousePadMesh")
    obj = bpy.data.objects.new("MousePad", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh for rounded corners
    bm = bmesh.new()

    # Create the base rectangle with rounded corners
    geom = bmesh.ops.create_circle(bm, cap_tris=True, radius=corner_radius, segments=16)
    bmesh.ops.scale(bm, vec=(length, width, 1), verts=geom['verts'])

    # Create the top and bottom faces
    top_face = bmesh.ops.create_circle(bm, cap_tris=True, radius=corner_radius, segments=16)
    bmesh.ops.scale(bm, vec=(length, width, 1), verts=top_face['verts'])

    # Create the side faces
    for v in geom['verts']:
        v.co.z = thickness

    # Create faces
    bmesh.ops.face_create(bm, verts=[v for v in geom['verts']])  # Bottom face
    bmesh.ops.face_create(bm, verts=[v for v in top_face['verts']])  # Top face

    # Link the side faces
    for i in range(len(geom['verts'])):
        bmesh.ops.face_create(bm, verts=[geom['verts'][i], geom['verts'][(i + 1) % len(geom['verts'])], top_face['verts'][(i + 1) % len(top_face['verts'])], top_face['verts'][i]])

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