import bpy
import bmesh

def create_dumbbell():
    # Create two spheres for the ends of the dumbbell
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 1))
    sphere1 = bpy.context.object
    sphere1.name = "Dumbbell_End_1"
    
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, -1))
    sphere2 = bpy.context.object
    sphere2.name = "Dumbbell_End_2"
    
    # Create a cylinder for the central shaft
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2, location=(0, 0, 0))
    shaft = bpy.context.object
    shaft.name = "Dumbbell_Shaft"
    
    # Join the objects to make a single dumbbell mesh
    bpy.ops.object.select_all(action='DESELECT')
    sphere1.select_set(True)
    sphere2.select_set(True)
    shaft.select_set(True)
    bpy.context.view_layer.objects.active = shaft
    bpy.ops.object.join()
    
create_dumbbell()