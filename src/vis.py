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
    EXP_ROOT = "./exp/full/chair/"
    
    st.title("LLM 3D Zero-shot One-run Single-shape Synthesis Experiment")
    
    # 实验选择与基础信息双列布局
    col_meta = st.columns([2, 3])
    with col_meta[0]:
        experiments = [d for d in os.listdir(EXP_ROOT) 
                      if os.path.isdir(os.path.join(EXP_ROOT, d))]
        selected_exp = st.selectbox("Choose exp folder", experiments)
    
    exp_dir = os.path.join(EXP_ROOT, selected_exp)
    data = load_experiment_data(exp_dir)
    
    with col_meta[1]:
        st.subheader("Description Summary")
        st.markdown(f'```\n{data["description"]}\n```')

    # 历史记录与反馈的三列布局
    if data["history"] or data["feedback"]:
        cols = st.columns([4, 3])
        with cols[0]:
            st.subheader("Raw History")
            st.json(data["history"], expanded=False)
        with cols[1]:
            st.subheader("Raw Feedbacks")
            st.json(data["feedback"], expanded=False)
        # with cols[2]:
        #     st.subheader("Metrics Summary")
        #     st.warning("Metrics visualization area")  # 可扩展指标图表

    # 迭代展示优化
    for iter_num in sorted(data["iterations"].keys()):
        st.divider()
        
        # 主内容区布局
        main_col, side_col = st.columns([3, 2])
        
        with main_col:
            st.subheader(f"Iteration {iter_num} Visualizations")
            img_cols = st.columns(4)
            for idx, img_file in enumerate(data["iterations"][iter_num]):
                try:
                    img = Image.open(os.path.join(exp_dir, img_file))
                    img_cols[idx].image(img, caption=f"Step {idx+1}", use_container_width=True)
                except Exception as e:
                    img_cols[idx].error(f"Image load error: {img_file}")
            
            with st.expander("Raw JSON Data"):
                    st.json({
                        "user_prompt": data["history"][iter_num * 2],
                        "assistant_response": data["history"][iter_num * 2 + 1]
                    })

        with side_col:
            st.subheader("Interaction Context")
            if data["history"] and len(data["history"]) > iter_num*2:
                history_iter = iter_num * 2
                
                with st.chat_message("user"):
                    st.caption("User Instruction")
                    with st.expander("Instruction Details"):
                        st.markdown(data["history"][iter_num]['content'])
                
                with st.chat_message("assistant"):
                    st.caption("VLM Feedback")
                    st.markdown(data["feedback"][iter_num]['feedback'])

                # chat_cols = st.columns(2)
                
                # with chat_cols[0]:
                #     with st.chat_message("user"):
                #         st.caption("User Instruction")
                #         with st.expander("Instruction Details"):
                #             st.markdown(data["history"][history_iter]['content'])
                
                # with chat_cols[1]:
                #     with st.chat_message("assistant"):
                #         st.caption("VLM Feedback")
                #         st.markdown(data["feedback"][history_iter]['feedback'])
                
                # with st.expander("Raw JSON Data"):
                #     st.json({
                #         "user_prompt": data["history"][history_iter],
                #         "assistant_response": data["history"][history_iter+1]
                #     })
            else:
                st.info("No conversation record for this iteration")

if __name__ == "__main__":
    main()