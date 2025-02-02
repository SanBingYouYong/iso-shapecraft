import bpy
import bmesh
from mathutils import Vector

def create_pizza_slice():
    # Define the vertices of the triangular pizza slice
    verts = [
        Vector((0, 0, 0)),  # Tip of the pizza slice
        Vector((1, 0, 0)),  # Right corner of the base
        Vector((0.5, 1, 0)),  # Left corner of the base
        Vector((0, 0, 0.2)),  # Tip of the pizza slice (thick crust)
        Vector((1, 0, 0.2)),  # Right corner of the base (thick crust)
        Vector((0.5, 1, 0.2))   # Left corner of the base (thick crust)
    ]
    
    # Define the faces using the vertices
    faces = [
        (0, 1, 2),  # Main triangular face
        (3, 4, 5),  # Top face for the crust
        (0, 1, 4, 3),  # Right crust face
        (1, 2, 5, 4),  # Bottom right crust face
        (2, 0, 3, 5)   # Left crust face
    ]
    
    # Create a new mesh
    mesh = bpy.data.meshes.new("PizzaSlice")
    obj = bpy.data.objects.new("PizzaSlice", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create the mesh from the vertices and faces
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    # Add a solidify modifier for the crust thickness
    modifier = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    modifier.thickness = 0.1  # Thickness of the crust

create_pizza_slice()