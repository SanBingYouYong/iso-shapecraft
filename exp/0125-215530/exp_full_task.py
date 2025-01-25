import bpy
import bmesh

def create_hexagonal_prism(base_edge_length, height):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new("HexagonalPrism")
    obj = bpy.data.objects.new("HexagonalPrism", mesh)

    # Link the object to the scene
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to build the geometry
    bm = bmesh.new()

    # Define the vertices for a hexagon
    vertices = []
    for i in range(6):
        angle = i * (360 / 6) * (3.14159 / 180)  # Convert degrees to radians
        x = base_edge_length * 0.5 * (1 + (i % 2)) * (1 if i % 2 == 0 else 0.866)
        y = base_edge_length * 0.5 * (1 - (i % 2)) * (1 if i % 2 == 1 else 0.866)
        vertices.append(bm.verts.new((x, y, 0)))
        vertices.append(bm.verts.new((x, y, height)))

    # Create faces
    for i in range(6):
        bm.faces.new((vertices[i*2], vertices[(i*2+1) % 12], vertices[((i+1)*2+1) % 12], vertices[((i+1)*2) % 12]))

    # Finalize the mesh
    bm.to_mesh(mesh)
    bm.free()

# Parameters for the hexagonal prism
base_edge_length = 5
height = 15

create_hexagonal_prism(base_edge_length, height)import bpy
import math

def create_twisted_torus(major_radius, minor_radius, twist_angle):
    # Create a torus
    bpy.ops.mesh.primitive_torus_add(major_radius=major_radius, minor_radius=minor_radius, location=(0, 0, 0))
    torus = bpy.context.object
    
    # Apply twisting
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.rotate(value=math.radians(twist_angle), orient_axis='Z')
    bpy.ops.object.mode_set(mode='OBJECT')

# Parameters: major radius, minor radius, twist angle
create_twisted_torus(10, 3, 45)import bpy

def create_concentric_spheres():
    # Define the radii and colors for the spheres
    radii = [2, 4, 6]
    colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)]  # Red, Green, Blue

    for i, radius in enumerate(radii):
        # Create a new sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
        sphere = bpy.context.object
        
        # Set the material properties
        mat = bpy.data.materials.new(name=f"Material_{i}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = colors[i]
        bsdf.inputs['Roughness'].default_value = 0.8  # Matte finish
        
        # Assign the material to the sphere
        if sphere.data.materials:
            sphere.data.materials[0] = mat
        else:
            sphere.data.materials.append(mat)

create_concentric_spheres()