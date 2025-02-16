import streamlit as st
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import json
import os

from exp_single_data_extract_scad import ShapeFiles, get_shapefiles

st.set_page_config(layout="wide")

# 添加一个文本输入框来输入文件夹路径
folder_path = st.sidebar.text_input("输入文件夹路径", "exp/eval_python_single_10x_shapes_daily_4omini")

# 获取shape files
shape_files: List[ShapeFiles] = list(get_shapefiles(folder_path).values())

# 侧边栏选择器
selected_index = st.sidebar.selectbox(
    "选择要查看的Shape",
    options=[shape.shape_index for shape in shape_files],
    index=0
)

# 获取当前选中的ShapeFiles对象
selected_shape = next(shape for shape in shape_files if shape.shape_index == selected_index)

# 显示shape description
if selected_shape.shape_description and selected_shape.shape_description.exists():
    with open(selected_shape.shape_description, 'r') as f:
        description = f.read()
    st.subheader("形状描述")
    st.write(description)

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("预览图片")
    # 读取 evaluations.json 文件并显示最佳得分
    evaluations_file = selected_shape.evaluations_json
    if evaluations_file.exists():
        try:
            with open(evaluations_file, 'r') as f:
                evaluations = json.load(f)
            
            best_score = max(evaluations, key=lambda x: x[0])[0]
            best_score_file = next(x[1] for x in evaluations if x[0] == best_score)
            st.write(f"最佳得分: {best_score}")
            st.write(f"文件: {os.path.basename(best_score_file)}")
            best_image_path = os.path.splitext(best_score_file)[0] + "_0" + ".png"
            if os.path.exists(best_image_path):
                st.image(best_image_path, width=300, caption=os.path.basename(best_image_path))
        except Exception as e:
            st.error(f"加载 evaluations.json 文件失败: {str(e)}")
    else:
        st.warning(f"evaluations.json 文件不存在: {evaluations_file}")
    for png in selected_shape.png_files:
        if png.exists():
            st.image(str(png), width=300, caption=os.path.basename(png))
        else:
            st.warning(f"图片不存在: {png}")

with col2:
    st.subheader("历史记录")
    for history_file in selected_shape.history_jsons:
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
                
                # 假设历史记录格式为 {"messages": [{"role": "user", "content": "..."}, ...]}
                for msg in history:
                    with st.expander(f"Message from {msg.get('role', 'user')}"):
                        st.write(msg.get("content", ""))
            except Exception as e:
                st.error(f"加载历史文件失败 {history_file}: {str(e)}")
        else:
            st.warning(f"历史文件不存在: {history_file}")