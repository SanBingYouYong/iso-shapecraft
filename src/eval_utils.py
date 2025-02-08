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

# 使用示例
if __name__ == "__main__":
    file_path = "C:\\ZSY\\imperial\\courses\\ISO\\iso-shapecraft\\exp\\full\\chair\\aggregator\\0.obj"  # 替换为你的OBJ文件路径
    v_count, f_count = count_obj_vertices_faces(file_path)
    print(f"顶点数: {v_count}, 面数: {f_count}")