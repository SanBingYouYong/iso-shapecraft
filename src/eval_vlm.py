import os
import json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def collect_evaluation_scores(root_folder):
    # evaluation_data = defaultdict(lambda: defaultdict(int))

    plain_iteration_scores = {
        "0": [],
        "1": [],
        "2": [],
    }

    all_lines = []
    
    for dirpath, _, filenames in os.walk(root_folder):
        if 'evaluations.json' in filenames:
            eval_file = os.path.join(dirpath, 'evaluations.json')
            
            with open(eval_file, 'r', encoding='utf-8') as f:
                evaluations = json.load(f)

            evals = defaultdict(dict)
            
            for score, file_path in evaluations:
                base_name = os.path.basename(file_path)  # e.g., "0_0.py"
                base_name_no_ext = os.path.splitext(base_name)[0]  # e.g., "0_0"
                base_path, iteration = base_name_no_ext.rsplit('_', 1)  # e.g., "0", "0"

                plain_iteration_scores[iteration].append(score)

                evals[base_path][iteration] = score

            # all_lines will be appended each iteration's scores
            for base_path, scores in evals.items():
                line = [scores.get(str(i), 0) for i in range(3)]
                all_lines.append(line)
            
    return plain_iteration_scores, all_lines

def collect_all_data(root_folders: list):
    plain_iteration_scores = {
        "0": [],
        "1": [],
        "2": [],
    }

    all_lines = []

    for root_folder in root_folders:
        scores, lines = collect_evaluation_scores(root_folder)
        for key in plain_iteration_scores:
            plain_iteration_scores[key].extend(scores[key])
        all_lines.extend(lines)

    return plain_iteration_scores, all_lines

def plot_vlm_evaluations(plain_iteration_scores, all_lines):

    # Set the style for better-looking plots
    plt.style.use('seaborn-v0_8-paper')
    fig, axs = plt.subplots(1, 2, figsize=(24, 8))

    # Increase DPI for better quality
    fig.set_dpi(150)

    # First subplot - Line Plot (Excluding Zero Values)
    axs[0].set_facecolor('#f8f9fa')
    axs[0].grid(True, linestyle='--', alpha=0.7, color='white')

    overall_count = 0
    upward_count = 0
    x = np.arange(3)  # 3 points on x-axis

    for row in all_lines:
        row = [val for val in row if val != 0]
        if len(row) > 1:
            is_upward = row[-1] >= row[0]
            overall_count += 1

            if is_upward:
                upward_count += 1
                axs[0].plot(x[:len(row)], row, marker='o', markersize=8, 
                            linewidth=2.5, color='#00b4d8', alpha=0.7, 
                            markeredgecolor='white', markeredgewidth=1)
            else:
                axs[0].plot(x[:len(row)], row, marker='o', markersize=8, 
                            linewidth=2.5, color='#ff6b6b', alpha=0.5, 
                            markeredgecolor='white', markeredgewidth=1)
        else:
            axs[0].plot(x[:len(row)], row, marker='o', markersize=8, 
                            linewidth=2.5, color='#00b4d8', alpha=0.7, 
                            markeredgecolor='white', markeredgewidth=1)
    
    print(f"Upward trends: {upward_count}/{overall_count} ({upward_count / overall_count:.2%})")

    axs[0].set_title('All VLM Evaluation Scores', fontsize=16, fontweight='bold', pad=20)
    axs[0].set_xlabel('Iteration', fontsize=16, fontweight='bold')
    axs[0].set_ylabel('Average Evaluation Score (within each iteration)', fontsize=16, fontweight='bold')
    axs[0].set_xticks(x)
    axs[0].tick_params(axis='both', which='major', labelsize=14)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)
    axs[0].margins(y=0.1)
    upward_label = 'Upward Trend'
    downward_label = 'Downward Trend'
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = {upward_label: plt.Line2D([0], [0], color='#00b4d8', lw=2.5),
                downward_label: plt.Line2D([0], [0], color='#ff6b6b', lw=2.5)}
    axs[0].legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=14)

    # Second subplot - Bar Plot of Average Scores without Error Bars
    averages = {key: np.mean(values) for key, values in plain_iteration_scores.items()}
    positions = np.arange(len(averages))
    width = 0.6

    axs[1].set_facecolor('#f8f9fa')
    axs[1].grid(True, linestyle='--', alpha=0.7, color='white')
    bars = axs[1].bar(positions, averages.values(), width=width, alpha=0.8, color='#4361ee')

    for bar in bars:
        height = bar.get_height()
        axs[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=12, fontweight='bold', color='#333333')

    axs[1].set_xlabel("Iteration", fontsize=16, fontweight='bold')
    axs[1].set_ylabel("Average Evaluation Score (over iterations)", fontsize=16, fontweight='bold')
    axs[1].set_title("Average VLM Evaluation Scores", fontsize=16, fontweight='bold', pad=20)
    axs[1].set_xticks(positions)
    axs[1].set_xticklabels(averages.keys())
    axs[1].tick_params(axis='both', which='major', labelsize=14)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)
    axs[1].margins(y=0.1)
    axs[1].set_ylim(5, 5.5)

    plt.tight_layout(pad=3.0)
    plt.show()

if __name__ == "__main__":
    paths = [
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_single_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_10x_shapes_daily_4omini",        
    ]
    root_folder = "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini"
    # result = collect_evaluation_scores(root_folder)
    # print(result)
    plain_iteration_scores, all_lines = collect_all_data(paths)
    # plain_iteration_scores, all_lines = collect_evaluation_scores(root_folder)
    plot_vlm_evaluations(plain_iteration_scores, all_lines)
