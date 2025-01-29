import bpy
import math

def create_fan_shape(radius, num_lines):
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    empty = bpy.context.active_object

    for i in range(num_lines):
        angle = i * (2 * math.pi / num_lines)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=radius, location=(x/2, y/2, 0))
        obj = bpy.context.active_object
        obj.rotation_euler[2] = angle

    bpy.context.view_layer.objects.active = empty
    bpy.ops.object.select_all(action='DESELECT')
    empty.select_set(True)
    bpy.context.view_layer.objects.active = empty

create_fan_shape(radius=5, num_lines=12)