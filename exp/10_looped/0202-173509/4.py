import bpy
import bmesh
from mathutils import Vector

def create_pizza_slice():
    # Parameters for the pizza slice
    radius = 1.0
    crust_thickness = 0.2
    slice_angle = 60  # degrees
    slice_height = 0.2

    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name="PizzaSlice")
    obj = bpy.data.objects.new("PizzaSlice", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build geometry
    bm = bmesh.new()

    # Create outer vertices for the crust
    outer_verts = []
    for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
        rad = angle * (3.14159 / 180)  # Convert angle to radians
        outer_x = Vector((radius * (1 - (crust_thickness / radius)), 0, crust_thickness))  # Crust height
        outer_x.rotate(Vector((0, 0, rad)))  # Rotate around Z-axis
        outer_verts.append(bm.verts.new(outer_x))

    # Create inner vertices for the topping
    inner_verts = []
    for angle in range(-slice_angle // 2, slice_angle // 2 + 1):
        rad = angle * (3.14159 / 180)  # Convert angle to radians
        inner_x = Vector((radius * (1 - (crust_thickness / radius)), 0, 0))  # Base height
        inner_x.rotate(Vector((0, 0, rad)))  # Rotate around Z-axis
        inner_verts.append(bm.verts.new(inner_x))

    # Create faces for the pizza slice
    for i in range(len(outer_verts) - 1):
        bm.faces.new((outer_verts[i], outer_verts[i+1], inner_verts[i+1], inner_verts[i]))

    # Create the tip face
    bm.faces.new((inner_verts[0], inner_verts[-1], outer_verts[-1], outer_verts[0]))

    # Write the bmesh into the mesh and free bmesh
    bm.to_mesh(mesh)
    bm.free()

    # Move the pizza slice up to visualize it better
    obj.location.z += slice_height / 2

    # Set the object as active and select it
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

# Call the function to create the pizza slice
create_pizza_slice()