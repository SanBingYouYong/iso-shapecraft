import bpy

def create_hollow_ring(radius_outer, radius_inner, location):
    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=location, rotation=(0, 0, 0), major_radius=radius_outer, minor_radius=radius_outer - radius_inner)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')

create_hollow_ring(radius_outer=1, radius_inner=0.5, location=(0, 0, 0))