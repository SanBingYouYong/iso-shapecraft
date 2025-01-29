import bpy

def create_key_shape():
    # Create the rounded head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 1.5))
    head = bpy.context.object
    head.name = "KeyHead"
    
    # Create the long shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=3, location=(0, 0, 0))
    shaft = bpy.context.object
    shaft.name = "KeyShaft"
    
    # Join the head and shaft
    bpy.ops.object.select_all(action='DESELECT')
    head.select_set(True)
    shaft.select_set(True)
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.join()

create_key_shape()