import bpy

def create_bread_box():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the base of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
    base = bpy.context.object
    base.scale[0] = 0.9  # Width
    base.scale[1] = 0.5  # Depth
    base.scale[2] = 0.5  # Height

    # Create the lid of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.1))
    lid = bpy.context.object
    lid.scale[0] = 0.95  # Width (slightly wider)
    lid.scale[1] = 0.5   # Depth
    lid.scale[2] = 0.2   # Height (taller for better aesthetics)

    # Set the origin of the lid to the back for correct rotation
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.context.scene.cursor.location = (0, 0, 1.1)

    # Create a hinge for the lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.2, location=(0, -0.5, 1.1))
    hinge = bpy.context.object
    hinge.rotation_euler[0] = 1.5708  # Rotate to align with the lid

    # Parent the lid to the hinge for proper rotation
    lid.parent = hinge

    # Move the lid to sit flush with the top of the box
    lid.location.z += 0.05  # Adjust position slightly for better alignment

# Run the function to create the updated bread box
create_bread_box()