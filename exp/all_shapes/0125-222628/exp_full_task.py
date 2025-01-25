import bpy
import math

def create_cone_with_groove(base_radius=5, height=12, groove_depth=0.2, turns=10):
    # Create a cone
    bpy.ops.mesh.primitive_cone_add(radius1=base_radius, depth=height, location=(0, 0, height / 2))
    cone = bpy.context.active_object
    
    # Add a spiral groove
    for i in range(turns * 100):
        angle = i * (2 * math.pi / 100)  # Angle for each segment
        z = (i / 100) * height  # Height position
        
        # Calculate the radius at this height
        radius = base_radius * (1 - (z / height))
        
        # Create a small circle for the groove
        bpy.ops.mesh.primitive_circle_add(radius=groove_depth, location=(radius * math.cos(angle), radius * math.sin(angle), z))
        groove = bpy.context.active_object
        
        # Add the groove to the cone
        bpy.ops.object.select_all(action='DESELECT')
        cone.select_set(True)
        groove.select_set(True)
        bpy.context.view_layer.objects.active = cone
        bpy.ops.object.join()
    
    # Rename the final object
    cone.name = "ConeWithGroove"

create_cone_with_groove()