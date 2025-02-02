import bpy

def create_shopping_bag():
    # Create the bag body
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    bag = bpy.context.object
    bag.scale[0] = 0.5  # Width
    bag.scale[1] = 0.3  # Depth
    bag.scale[2] = 1.0  # Height

    # Go to edit mode to modify the shape
    bpy.ops.object.mode_set(mode='EDIT')

    # Select the top face and scale it to create a tapered effect
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_face_by_sides(number=4, extend=False)  # Select the top face
    bpy.ops.transform.resize(value=(0.8, 0.8, 1))  # Slightly scale down the top face

    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Create the handles using extrusion
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Select the top edge loop for extrusion
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    # Select the top edge loops for the handles
    top_edges = [v for v in bag.data.vertices if v.co.z >= 0.9]  # Find top vertices
    for edge in bag.data.edges:
        if edge.verts[0] in top_edges and edge.verts[1] in top_edges:
            edge.select = True

    # Extrude and scale handles
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0.5, 0)})
    bpy.ops.transform.resize(value=(1, 0.2, 0.2))  # Scale the handles
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, -0.5, 0)})

    # Go back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

create_shopping_bag()