import bpy
import bmesh
from mathutils import Vector

def create_pizza_slice():
    # Define the vertices of the triangular pizza slice with an improved triangular shape and pronounced crust
    verts = [
        Vector((0, 0, 0)),        # Tip of the pizza slice
        Vector((1.5, 0, 0)),      # Right corner of the base (wider base)
        Vector((0.5, 1, 0)),      # Left corner of the base (higher for triangle shape)
        Vector((0, 0, 0.3)),      # Tip of the pizza slice (thick crust)
        Vector((1.5, 0, 0.3)),    # Right corner of the base (thick crust)
        Vector((0.5, 1, 0.3)),    # Left corner of the base (thick crust)
        Vector((0.1, -0.1, 0.5)),  # Additional vertex for rounded crust elevation
        Vector((1.4, -0.1, 0.5))   # Additional vertex for rounded crust elevation
    ]
    
    # Define the faces using the vertices
    faces = [
        (0, 1, 2),          # Main triangular face
        (3, 4, 5),          # Top face for the crust
        (0, 1, 4, 3),      # Right crust face
        (1, 2, 5, 4),      # Bottom right crust face
        (2, 0, 3, 5),      # Left crust face
        (3, 6, 7, 4)       # Rounded outer crust face
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
    modifier.thickness = 0.3  # Increased thickness for a more pronounced crust

    # Optionally, apply a bevel to the edges for a more organic shape
    bevel_modifier = obj.modifiers.new(name="Bevel", type='BEVEL')
    bevel_modifier.width = 0.05  # Adjust the bevel width for a softer edge

create_pizza_slice()