import bpy

def create_beveled_cube(edge_length=10, bevel_radius=1):
    # Delete the default cube
    if "Cube" in bpy.data.objects:
        bpy.data.objects["Cube"].select_set(True)
        bpy.ops.object.delete()
    
    # Create a new cube
    bpy.ops.mesh.primitive_cube_add(size=edge_length)
    cube = bpy.context.active_object
    
    # Apply bevel to the cube's edges
    bpy.ops.object.modifier_add(type='BEVEL')
    cube.modifiers["Bevel"].width = bevel_radius
    cube.modifiers["Bevel"].segments = 10  # Adjust segments for smoothness
    bpy.ops.object.modifier_apply(modifier="Bevel")

create_beveled_cube()