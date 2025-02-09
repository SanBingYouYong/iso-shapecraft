import os


def count_obj_vertices_faces(obj_file_path):
    """
    读取OBJ文件并返回顶点数和面数。
    
    参数:
        obj_file_path (str): OBJ文件的路径
        
    返回:
        tuple: (顶点数, 面数)
    """
    vertices = 0
    faces = 0
    
    with open(obj_file_path, 'r') as file:
        for line in file:
            # 去除前后空白并分割
            stripped_line = line.strip()
            if not stripped_line:
                continue  # 跳过空行
            
            # 检查顶点行（以'v '开头）
            if stripped_line.startswith('v '):
                vertices += 1
            # 检查面行（以'f '开头）
            elif stripped_line.startswith('f '):
                faces += 1
                
    return vertices, faces

def find_obj_and_count(folder_path):
    """
    查找文件夹中的所有OBJ文件并返回它们的顶点数和面数。
    
    参数:
        folder_path (str): 包含OBJ文件的文件夹路径
        
    返回:
        dict: 包含文件名和对应顶点数和面数的字典
    """
    obj_counts = {}
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.obj'):
                obj_file_path = os.path.join(root, file)
                v_count, f_count = count_obj_vertices_faces(obj_file_path)
                obj_counts[obj_file_path] = (v_count, f_count)
                
    return obj_counts

# 使用示例
if __name__ == "__main__":
    file_path = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scad_exp_3x_shapes_daily_4omini\shape_0000\855161a1aaba30c2b4b1aa7f729e2961\e403e5c5cc19a213991df87c33a2b180.obj"  # 替换为你的OBJ文件路径
    v_count, f_count = count_obj_vertices_faces(file_path)
    print(f"顶点数: {v_count}, 面数: {f_count}")
    # counts = find_obj_and_count("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\scad_exp_3x_shapes_daily_4omini")  # 替换为你的文件夹路径
    # print(f"找到{len(counts)}个OBJ文件")
    # average_v_count = sum(v_count for v_count, _ in counts.values()) / len(counts)
    # average_f_count = sum(f_count for _, f_count in counts.values()) / len(counts)
    # print(f"平均顶点数: {average_v_count}, 平均面数: {average_f_count}")
