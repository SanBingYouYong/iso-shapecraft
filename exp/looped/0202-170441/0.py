import bpy

def create_wedge(length, width, height):
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Scale the cube to form a wedge
    bpy.ops.transform.resize(value=(length, width, height))
    
    # Select the top face and scale it down to create the tapered end
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_face_by_index(index=4)  # Select the top face
    bpy.ops.transform.resize(value=(0.1, 0.1, 1))  # Taper the top
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    
create_wedge(2, 1, 0.5)