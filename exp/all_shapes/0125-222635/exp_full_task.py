import bpy
import math

def create_intersecting_cubes():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    # Create the first cube
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 0))
    cube1 = bpy.context.object

    # Create the second cube, rotated at 45 degrees
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 0))
    cube2 = bpy.context.object
    cube2.rotation_euler[0] = math.radians(45)  # Rotate around X-axis

    # Select both cubes to ensure they are visible in the scene
    bpy.ops.object.select_all(action='DESELECT')
    cube1.select_set(True)
    cube2.select_set(True)

create_intersecting_cubes()