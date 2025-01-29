import bpy

def create_diagonal_cross():
    # Create the first line of the cross
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=2, location=(0, 0, 0))
    line1 = bpy.context.active_object
    line1.rotation_euler = (0, 0, 0.785398)  # Rotate 45 degrees

    # Create the second line of the cross
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=2, location=(0, 0, 0))
    line2 = bpy.context.active_object
    line2.rotation_euler = (0, 0, -0.785398)  # Rotate -45 degrees

create_diagonal_cross()