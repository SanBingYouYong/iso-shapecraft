import os
import yaml
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np

def collect_paths(root_folder):
    '''
    Extract paths from all subfolders in the root folder, for subfolders containing image files and txt file
    '''
    clip_file = 'clip_similarity.yml'
    paths = []
    for root, dirs, files in os.walk(root_folder):
        if clip_file in files:
            paths.append(os.path.join(root, clip_file))
    return paths

def collect_data_for(root_dir):
    """
    Recursively search for clip_similarity.yml files starting from `root_dir`,
    parse the entries of the form:
    
        {path}_{iteration}_{id}.png: similarity_score
        
    Group the scores by path and iteration, and return the collected data.
    
    Parameters:
        root_dir (str): The root directory to start searching from.
    """
    # data[path][iteration] will be a list of similarity scores
    data = []

    collected_paths = collect_paths(root_dir)
    
    for yml_path in collected_paths:
        try:
            with open(yml_path, 'r') as f:
                content = yaml.safe_load(f)
        except Exception as e:
            print(f"Error reading {yml_path}: {e}")
            continue

        path_data = {}
        
        # Parse each entry in the YAML file
        for key, sim_value in content.items():
            # Remove the '.png' extension and split by underscore.
            base = key.replace('.png', '')
            parts = base.split('_')
            if len(parts) != 3:
                continue  # Skip if key doesn't match the expected format.
            try:
                # First number is the path, second is the iteration.
                path_id = int(parts[0])
                iteration = int(parts[1])
            except ValueError:
                continue
            if path_id not in path_data:
                path_data[path_id] = {}
            if iteration not in path_data[path_id]:
                path_data[path_id][iteration] = []
            path_data[path_id][iteration].append(sim_value)
        
        data.append(path_data)
    return data

def collect_data_multiple(root_dirs):
    """
    Collect data for multiple root directories.
    
    Parameters:
        root_dirs (list): A list of root directories to collect data from.
    """
    all_data = []
    for root_dir in root_dirs:
        all_data.extend(collect_data_for(root_dir))
    return all_data

def plot_clip_similarity(data):
    """
    Plot the CLIP similarity scores.

    Parameters:
        data (list): A list of dictionaries containing the collected data.
    """
    upward_count = 0
    overall_count = 0

    # Set the style for better-looking plots
    plt.style.use('seaborn-v0_8-paper')
    fig, axs = plt.subplots(1, 2, figsize=(24, 8))

    # Increase DPI for better quality
    fig.set_dpi(150)

    # First subplot - Path Performance
    cmap = plt.get_cmap("tab10")
    num_colors = 10

    # Add a light gray background grid
    axs[0].set_facecolor('#f8f9fa')
    axs[0].grid(True, linestyle='--', alpha=0.7, color='white')

    for idx, path_data in enumerate(data):
        for path_id, iter_dict in path_data.items():
            iterations = sorted(iter_dict.keys())
            avg_scores = [np.mean(iter_dict[it]) for it in iterations]
            is_upward = avg_scores[-1] >= avg_scores[0]
            overall_count += 1
            
            if is_upward:
                upward_count += 1
                axs[0].plot(iterations, avg_scores, marker='o', markersize=8, 
                        linewidth=2.5, color='#00b4d8', label=f'Path {path_id}',
                        alpha=0.7, markeredgecolor='white', markeredgewidth=1)
            else:
                axs[0].plot(iterations, avg_scores, marker='o', markersize=8,
                        linewidth=2.5, color='#ff6b6b', alpha=0.5,
                        markeredgecolor='white', markeredgewidth=1)

    print(f"Upward trends: {upward_count}/{overall_count} ({upward_count / overall_count:.2%})")

    # Enhance first subplot appearance
    axs[0].set_ylabel("Average CLIP Score (within each iteration)", fontsize=16, fontweight='bold')
    axs[0].set_xlabel("Iterations", fontsize=16, fontweight='bold')
    axs[0].set_xticks(iterations)
    axs[0].set_title("All CLIP Scores", fontsize=16, fontweight='bold', pad=20)
    axs[0].tick_params(axis='both', which='major', labelsize=14)
    axs[0].spines['top'].set_visible(False)
    axs[0].spines['right'].set_visible(False)
    upward_label = 'Upward Trend'
    downward_label = 'Downward Trend'
    handles, labels = axs[0].get_legend_handles_labels()
    by_label = {upward_label: plt.Line2D([0], [0], color='#00b4d8', lw=2.5),
                downward_label: plt.Line2D([0], [0], color='#ff6b6b', lw=2.5)}
    axs[0].legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=14)

    # Second subplot - CLIP Similarity
    # Calculate statistics
    all_scores = {}
    for path_data in data:
        for path_id, iter_dict in path_data.items():
            for iteration, scores in iter_dict.items():
                if iteration not in all_scores:
                    all_scores[iteration] = []
                all_scores[iteration].extend(scores)

    iterations = sorted(all_scores.keys())
    avg_scores = [np.mean(all_scores[it]) for it in iterations]
    std_devs = [np.std(all_scores[it]) for it in iterations]

    # Enhanced bar plot
    positions = np.arange(len(iterations))
    width = 0.6  # Increased width for better visibility

    # Add background grid
    axs[1].set_facecolor('#f8f9fa')
    axs[1].grid(True, linestyle='--', alpha=0.7, color='white')
    # Create bars with gradient color
    bars = axs[1].bar(positions, avg_scores, width=width, alpha=0.8, color='#4361ee')

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        axs[1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', fontsize=10)

    # Enhance second subplot appearance
    axs[1].set_ylim(0.3, 0.32)  # Slightly expanded y-range for better visualization
    axs[1].set_xlabel("Iteration", fontsize=16, fontweight='bold')
    axs[1].set_ylabel("Average CLIP Score (over iterations)", fontsize=16, fontweight='bold')
    axs[1].set_title("Average CLIP Score", fontsize=16, fontweight='bold', pad=20)
    axs[1].set_xticks(positions)
    axs[1].set_xticklabels(iterations)
    axs[1].tick_params(axis='both', which='major', labelsize=14)
    axs[1].spines['top'].set_visible(False)
    axs[1].spines['right'].set_visible(False)

    # Overall figure adjustments
    plt.tight_layout(pad=3.0)
    plt.show()

# Example usage:
# plot_clip_similarity('/path/to/your/root/folder')


if __name__ == "__main__":
    paths = [
        # "exp/eval_python_full_10x_shapes_daily_4omini",
        # "exp/eval_python_single_10x_shapes_daily_4omini",
        # "exp/eval_scad_full_3x_shapes_daily_multistruct_4omini",
        # "exp/eval_scad_full_3x_shapes_primitive_multi_4omini",
        # "exp/eval_scad_full_10x_shapes_daily_4omini",
        # "exp/eval_scad_single_3x_shapes_daily_multistruct_4omini",
        # "exp/eval_scad_single_3x_shapes_primitive_multi_4omini",
        # "exp/eval_scad_single_10x_shapes_daily_4omini",      
        "exp/cadprompt_test_10x_cadprompt_parsed"  
    ]
    paths = [os.path.abspath(p) for p in paths]
    # data = collect_data_for(paths[0])
    data = collect_data_multiple(paths)
    plot_clip_similarity(data)
