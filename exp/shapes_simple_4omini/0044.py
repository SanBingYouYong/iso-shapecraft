import bpy

def create_arrow():
    # Create the shaft of the arrow
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(0, 0, 0))
    shaft = bpy.context.object
    shaft.name = 'Arrow_Shaft'
    
    # Create the tip of the arrow
    bpy.ops.mesh.primitive_cone_add(radius1=0.3, depth=0.5, location=(0, 0, 1))
    tip = bpy.context.object
    tip.name = 'Arrow_Tip'
    
    # Combine the shaft and tip into one object
    bpy.ops.object.select_all(action='DESELECT')
    shaft.select_set(True)
    tip.select_set(True)
    bpy.context.view_layer.objects.active = shaft
    bpy.ops.object.join()
    
    # Rename the final arrow object
    arrow = bpy.context.object
    arrow.name = 'Arrow'

create_arrow()