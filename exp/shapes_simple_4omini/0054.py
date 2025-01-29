import bpy

def create_grid(rows, cols, square_size):
    for row in range(rows):
        for col in range(cols):
            x = col * square_size
            y = row * square_size
            bpy.ops.mesh.primitive_plane_add(size=square_size, location=(x, y, 0))

create_grid(5, 5, 1)