import bpy

def create_cylinder(outer_radius, wall_thickness, height):
    # Calculate inner radius
    inner_radius = outer_radius - wall_thickness

    # Create the outer cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=outer_radius, depth=height, location=(0, 0, height / 2))
    outer_cylinder = bpy.context.object

    # Create the inner cylinder (to subtract from the outer cylinder)
    bpy.ops.mesh.primitive_cylinder_add(radius=inner_radius, depth=height + 0.1, location=(0, 0, height / 2))
    inner_cylinder = bpy.context.object

    # Select both objects and join them
    bpy.ops.object.select_all(action='DESELECT')
    outer_cylinder.select_set(True)
    inner_cylinder.select_set(True)
    bpy.context.view_layer.objects.active = outer_cylinder

    # Use Boolean modifier to create a hollow cylinder
    bpy.ops.object.modifier_add(type='BOOLEAN')
    outer_cylinder.modifiers["Boolean"].operation = 'DIFFERENCE'
    outer_cylinder.modifiers["Boolean"].object = inner_cylinder
    bpy.ops.object.modifier_apply(modifier="Boolean")

    # Delete the inner cylinder
    bpy.data.objects.remove(inner_cylinder)

# Create a cylinder with specified dimensions
create_cylinder(7, 1, 20)