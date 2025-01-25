import bpy
import bmesh
from math import radians

def create_hexagonal_prism(edge_length=5, height=15):
    # Create a new mesh
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)
    
    # Link the object to the scene
    bpy.context.collection.objects.link(obj)
    
    # Create a bmesh for the hexagonal prism
    bm = bmesh.new()
    
    # Calculate the vertices of the hexagon
    vertices = []
    for i in range(6):
        angle = radians(60 * i)
        x = edge_length * cos(angle)
        y = edge_length * sin(angle)
        vertices.append((x, y, 0))  # Base vertices
        vertices.append((x, y, height))  # Top vertices

    # Create the vertices in the bmesh
    verts = [bm.verts.new(v) for v in vertices]
    bm.verts.ensure_lookup_table()
    
    # Create faces for the base and top
    bm.faces.new(verts[:6])  # Base face
    bm.faces.new(verts[6:])  # Top face
    
    # Create side faces
    for i in range(6):
        bm.faces.new((verts[i], verts[(i + 1) % 6], verts[(i + 1) % 6 + 6], verts[i + 6]))
    
    # Finish the bmesh and update the mesh
    bm.to_mesh(mesh)
    bm.free()
    
    # Set shading to smooth
    bpy.ops.object.shade_smooth()
    
create_hexagonal_prism()import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, location=(0, 0, 0))
    torus = bpy.context.object

    # Apply the twist
    bpy.ops.object.select_all(action='DESELECT')
    torus.select_set(True)
    bpy.context.view_layer.objects.active = torus
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
    
    # Rotate the torus around the Z axis to create the twist
    torus.rotation_euler[2] += math.radians(twist_angle)

# Create a torus with specified parameters
create_twisted_torus(major_radius=10, minor_radius=3, twist_angle=45)import bpy

def create_concentric_spheres():
    radii = [2, 4, 6]
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue

    for i, radius in enumerate(radii):
        # Create a new sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.object
        
        # Create a new material
        material = bpy.data.materials.new(name=f"Material_{i}")
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = colors[i]  # Set color
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        
        # Assign the material to the sphere
        if sphere.data.materials:
            sphere.data.materials[0] = material
        else:
            sphere.data.materials.append(material)

create_concentric_spheres()