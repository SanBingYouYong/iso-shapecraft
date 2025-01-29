import bpy
import math

def create_spiraling_cone(base_radius=5, height=12, turns=5, groove_depth=0.5):
    # Create a cone
    bpy.ops.mesh.primitive_cone_add(radius1=base_radius, depth=height)
    cone = bpy.context.object
    cone.name = "SpiralingCone"

    # Add a new mesh for the groove
    groove_mesh = bpy.data.meshes.new("GrooveMesh")
    groove_object = bpy.data.objects.new("Groove", groove_mesh)

    bpy.context.collection.objects.link(groove_object)

    vertices = []
    faces = []
    
    # Create vertices for the groove
    for i in range(100):
        angle = (i / 100) * (turns * 2 * math.pi)
        z = (i / 100) * height
        r = base_radius - (groove_depth * (i / 100))
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        vertices.append((x, y, z))

    # Create faces for the groove (connecting the vertices)
    for i in range(len(vertices) - 1):
        if i < len(vertices) - 2:
            faces.append((i, i + 1, i + 2))
    
    groove_mesh.from_pydata(vertices, [], faces)
    groove_mesh.update()

create_spiraling_cone()