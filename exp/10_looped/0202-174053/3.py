import bpy

def create_clock():
    # Clear existing mesh objects in the scene
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
    
    # Rotate the clock hand to point to 12 o'clock
    clock_hand.rotation_euler[0] = 0  # X-axis rotation
    clock_hand.rotation_euler[1] = 0  # Y-axis rotation
    clock_hand.rotation_euler[2] = 0  # Z-axis rotation (12 o'clock position)

    # Ensure the hand is properly oriented
    bpy.ops.object.origin_set(type='ORIGIN_BOTTOM', center='MEDIAN')

# Ensure the script runs only when executed in Blender
if __name__ == "__main__":
    create_clock()