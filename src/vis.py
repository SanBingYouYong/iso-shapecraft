import os
import json
import streamlit as st
from PIL import Image
from pathlib import Path

def load_experiment_data(exp_dir):
    """加载单个实验文件夹的数据"""
    data = {
        "iterations": {},
        "description": "",
        "history": None,
        "feedback": None
    }
    
    # 加载文本描述
    desc_path = os.path.join(exp_dir, "shape_description.txt")
    if os.path.exists(desc_path):
        with open(desc_path, "r") as f:
            data["description"] = f.read()
    
    # 加载历史记录
    for json_file in ["history.json", "feedback.json"]:
        path = os.path.join(exp_dir, json_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                data[json_file.split(".")[0]] = json.load(f)
    
    # 组织迭代数据
    img_files = sorted([f for f in os.listdir(exp_dir) if f.endswith(".png")])
    
    # 按迭代分组图片
    iterations = {}
    for img in img_files:
        base = img.split("_")[0]
        if base.isdigit():
            iter_num = int(base)
            if iter_num not in iterations:
                iterations[iter_num] = []
            iterations[iter_num].append(img)
    
    # 排序并存储迭代数据
    for iter_num in sorted(iterations.keys()):
        data["iterations"][iter_num] = sorted(
            iterations[iter_num],
            key=lambda x: int(Path(x).stem.split("_")[-1])
        )
    
    return data

def main():
    st.set_page_config(layout="wide")
    
    # 实验根目录设置（根据实际路径修改）
    EXP_ROOT = "./exp/single_daily_shapes_looped_all_0202-221821"
    
    st.title("LLM 3D生成实验分析")
    
    # 选择实验目录
    experiments = [d for d in os.listdir(EXP_ROOT) 
                  if os.path.isdir(os.path.join(EXP_ROOT, d))]
    selected_exp = st.selectbox("选择实验文件夹", experiments)
    exp_dir = os.path.join(EXP_ROOT, selected_exp)
    
    # 加载数据
    data = load_experiment_data(exp_dir)
    
    # 显示基础信息
    st.subheader("形状描述")
    st.text_area("", data["description"], height=100, disabled=True)
    
    # 并列显示历史记录
    if data["history"] or data["feedback"]:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("生成历史")
            st.json(data["history"], expanded=False)
        with col2:
            st.subheader("反馈记录") 
            st.json(data["feedback"], expanded=False)
    
    # 显示每个迭代的视觉结果
    st.divider()
    for iter_num in sorted(data["iterations"].keys()):
        st.subheader(f"迭代 {iter_num}")
        
        # 图片展示
        cols = st.columns(4)  # 4张图片并排
        for idx, img_file in enumerate(data["iterations"][iter_num]):
            img_path = os.path.join(exp_dir, img_file)
            try:
                img = Image.open(img_path)
                cols[idx].image(img, caption=img_file, use_container_width=True)
            except Exception as e:
                cols[idx].error(f"无法加载图片: {img_file}")
        
        history_iter = 2 * iter_num
        
        # 显示对应聊天记录
        if data["history"] and len(data["history"]) > iter_num:
            with st.expander(f"查看迭代 {iter_num} 的对话记录"):
                with st.chat_message('user'):
                    st.markdown(data["history"][history_iter]['content'])
                with st.chat_message('assistant'):
                    st.markdown(data["history"][history_iter+1]['content'])
                # st.markdown(data["history"][iter_num])
                # st.markdown(data["history"][iter_num+1])

if __name__ == "__main__":
    main()
