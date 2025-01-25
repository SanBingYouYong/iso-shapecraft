import bpy
import math
from mathutils import Vector

def create_star_prism(radius, height, points):
    # Create the star base
    star_points = []
    for i in range(points * 2):
        angle = math.pi * i / points
        r = radius if i % 2 == 0 else radius / 2
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        star_points.append((x, y, 0))

    # Create the mesh
    mesh = bpy.data.meshes.new("StarPrism")
    obj = bpy.data.objects.new("StarPrism", mesh)

    bpy.context.collection.objects.link(obj)

    # Create geometry
    vertices = star_points + [(x, y, height) for x, y, z in star_points]
    faces = []

    # Create bottom face
    bottom_face = [i for i in range(points * 2)]
    faces.append(bottom_face)

    # Create side faces
    for i in range(points * 2):
        next_index = (i + 1) % (points * 2)
        faces.append([i, next_index, next_index + points * 2, i + points * 2])

    # Create top face
    top_face = [i + points * 2 for i in range(points * 2)]
    faces.append(top_face)

    # Create mesh from vertices and faces
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

create_star_prism(6, 10, 8)