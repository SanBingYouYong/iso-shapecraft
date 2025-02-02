import bpy

def create_mouse_pad(length=0.3, width=0.2, thickness=0.01, corner_radius=0.02):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("MousePadMesh")
    obj = bpy.data.objects.new("MousePad", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create the geometry for the mouse pad
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Create a rounded rectangle using a plane
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    plane = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select all vertices and subdivide
    bpy.ops.mesh.subdivide(number_cuts=20)
    
    # Scale the plane
    bpy.ops.transform.resize(value=(length / 2, width / 2, 1))
    
    # Switch to vertex select mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Select corners and use loop cut for rounding
    for i in range(4):
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.loop_select()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.transform.vertex_random(offset=0, seed=0, scale=corner_radius)
        
    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Extrude to create thickness
    bpy.ops.object.modifier_add(type='SOLIDIFY')
    bpy.context.object.modifiers["Solidify"].thickness = thickness
    bpy.ops.object.modifier_apply(modifier="Solidify")

    # Add a material with texture
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