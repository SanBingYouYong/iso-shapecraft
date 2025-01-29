import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, 
                                      location=(0, 0, 0), rotation=(0, 0, 0))
    torus = bpy.context.active_object
    
    # Apply the twist
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    
    # Twist the torus along its central axis
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.rotate(value=math.radians(twist_angle), orient_axis='Z')
    bpy.ops.object.mode_set(mode='OBJECT')

# Parameters
major_radius = 10
minor_radius = 3
twist_angle = 45

create_twisted_torus(major_radius, minor_radius, twist_angle)