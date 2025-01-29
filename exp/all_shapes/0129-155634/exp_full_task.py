import bpy
import math

def create_intersecting_cubes():
    # Clear existing mesh objects
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    
    # Create first cube
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 0))
    cube1 = bpy.context.object
    
    # Create second cube, rotated 45 degrees around the Z axis
    bpy.ops.mesh.primitive_cube_add(size=6, location=(0, 0, 0))
    cube2 = bpy.context.object
    cube2.rotation_euler[2] = math.radians(45)
    
create_intersecting_cubes()