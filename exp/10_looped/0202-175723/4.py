import bpy

def create_bread_box():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the base of the bread box with more balanced proportions
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.4))
    base = bpy.context.object
    base.scale[0] = 1.0  # Width
    base.scale[1] = 0.6  # Depth
    base.scale[2] = 0.4  # Height

    # Create the lid of the bread box
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.8))
    lid = bpy.context.object
    lid.scale[0] = 1.0  # Width
    lid.scale[1] = 0.6  # Depth
    lid.scale[2] = 0.2  # Height

    # Set the origin of the lid to the back for correct rotation
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
    bpy.context.scene.cursor.location = (0, 0, 0.8)

    # Create a smaller hinge for the lid
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.1, location=(0, -0.3, 0.8))
    hinge = bpy.context.object
    hinge.rotation_euler[0] = 1.5708  # Rotate to align with the lid

    # Parent the lid to the hinge for proper rotation
    lid.parent = hinge

    # Adjust the lid's position to ensure it looks like it can open
    lid.location.z += 0.05  # Adjust position slightly for better alignment

    # Add a slight rotation to indicate the lid is open (for visual effect)
    lid.rotation_euler[0] = 0.2  # Slightly open the lid

# Run the function to create the updated bread box
create_bread_box()