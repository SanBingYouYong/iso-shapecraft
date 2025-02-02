import bpy

def create_clock():
    # Clear all mesh objects from the scene
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete(use_global=False)
    
    # Create the clock base (a cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=0.1, location=(0, 0, 0))
    clock_base = bpy.context.object
    clock_base.name = 'Clock Base'
    
    # Create the clock face (a UV sphere)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0.05))
    clock_face = bpy.context.object
    clock_face.name = 'Clock Face'
    
    # Create the clock hand (a narrow cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1, location=(0, 0, 0.5))
    clock_hand = bpy.context.object
    clock_hand.name = 'Clock Hand'
    
    # Rotate the clock hand to point to the 12 o'clock position
    clock_hand.rotation_euler[0] = 0  # X-axis
    clock_hand.rotation_euler[1] = 0  # Y-axis
    clock_hand.rotation_euler[2] = 0  # Z-axis

    # Set the origin of the clock hand to its bottom
    bpy.ops.object.origin_set(type='ORIGIN_BOTTOM', center='MEDIAN')

# Run the function
create_clock()