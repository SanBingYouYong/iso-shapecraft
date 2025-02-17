import os
import json
import yaml
from tqdm import tqdm


CLIP_SCORE_FILE = 'clip_similarity.yml'
VLM_EVALUATION_FILE = 'evaluations.json'


def tell_full_or_single(datapath: str):
    return "full" in datapath and "single" not in datapath

def tell_aggregation_or_subtask(folderpath: str):
    return "aggregator" in folderpath and "sub_task_" not in folderpath

def get_clip_scores(root_folder: str):
    clip_scores = []
    best_clip_scores = []
    
    for dirpath, _, filenames in os.walk(root_folder):
        if CLIP_SCORE_FILE in filenames:
            clip_file = os.path.join(dirpath, CLIP_SCORE_FILE)
            
            with open(clip_file, 'r') as f:
                clip_data = yaml.safe_load(f)
            
            best_score = 0
            for _, score in clip_data.items():
                clip_scores.append(score)
                if score > best_score:
                    best_score = score
            best_clip_scores.append(best_score)

    return best_clip_scores, clip_scores

def get_vlm_scores(root_folder: str):
    eval_best_scores = []
    eval_all_scores = []
    
    for dirpath, _, filenames in os.walk(root_folder):
        if VLM_EVALUATION_FILE in filenames:
            eval_file = os.path.join(dirpath, VLM_EVALUATION_FILE)
            
            with open(eval_file, 'r', encoding='utf-8') as f:
                evaluations = json.load(f)
            
            best_score = 0
            for evaluation in evaluations:
                eval_score = int(evaluation[0])
                eval_all_scores.append(eval_score)
                if eval_score > best_score:
                    best_score = eval_score
            
            eval_best_scores.append(best_score)
    return eval_best_scores, eval_all_scores

def calc_stat(data):
    if not data:
        return None, None, None

    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    stddev = variance ** 0.5

    return mean, variance, stddev

def eval_stat(path):
    best_clip_scores, clip_scores = get_clip_scores(path)
    best_vlm_scores, vlm_scores = get_vlm_scores(path)

    best_clip_mean, best_clip_var, best_clip_stddev = calc_stat(best_clip_scores)
    clip_mean, clip_var, clip_stddev = calc_stat(clip_scores)
    best_vlm_mean, best_vlm_var, best_vlm_stddev = calc_stat(best_vlm_scores)
    vlm_mean, vlm_var, vlm_stddev = calc_stat(vlm_scores)

    return {
        "best_clip_mean": best_clip_mean,
        "best_clip_var": best_clip_var,
        "best_clip_stddev": best_clip_stddev,
        "clip_mean": clip_mean,
        "clip_var": clip_var,
        "clip_stddev": clip_stddev,
        "best_vlm_mean": best_vlm_mean,
        "best_vlm_var": best_vlm_var,
        "best_vlm_stddev": best_vlm_stddev,
        "vlm_mean": vlm_mean,
        "vlm_var": vlm_var,
        "vlm_stddev": vlm_stddev,
    }

def eval_paths(paths):
    results = {}
    for path in tqdm(paths):
        results[path] = eval_stat(path)
    return results

def table_for_full_single(result):
    print("Path".ljust(50), "Best Clip".ljust(15), "Clip".ljust(15), "Best VLM".ljust(15), "VLM".ljust(15))
    for path, stat in result.items():
        best_clip = f"{stat['best_clip_mean']:.2f}/{stat['best_clip_stddev']:.2f}"
        clip = f"{stat['clip_mean']:.2f}/{stat['clip_stddev']:.2f}"
        best_vlm = f"{stat['best_vlm_mean']:.2f}/{stat['best_vlm_stddev']:.2f}"
        vlm = f"{stat['vlm_mean']:.2f}/{stat['vlm_stddev']:.2f}"
        
        print(os.path.basename(path).ljust(50), 
              best_clip.ljust(15), 
              clip.ljust(15), 
              best_vlm.ljust(15), 
              vlm.ljust(15))

def get_all_aggregator_and_subtask_folders(root_folder: str):
    aggregator_folders = []
    subtask_folders = []
    
    for dirpath, _, _ in os.walk(root_folder):
        if "aggregator" in dirpath:
            aggregator_folders.append(dirpath)
        elif "sub_task_" in dirpath:
            subtask_folders.append(dirpath)
    
    return aggregator_folders, subtask_folders

def get_clip_and_vlm_scores(folder: str):
    best_clip_scores, clip_scores = get_clip_scores(folder)
    best_vlm_scores, vlm_scores = get_vlm_scores(folder)
    
    return best_clip_scores, clip_scores, best_vlm_scores, vlm_scores

def eval_aggregator_vs_subtask(aggregator_folders, subtask_folders):
    aggregator_scores = []
    subtask_scores = []

    for folder in aggregator_folders:
        best_clip_scores, clip_scores, best_vlm_scores, vlm_scores = get_clip_and_vlm_scores(folder)
        aggregator_scores.append((best_clip_scores, clip_scores, best_vlm_scores, vlm_scores))

    for folder in subtask_folders:
        best_clip_scores, clip_scores, best_vlm_scores, vlm_scores = get_clip_and_vlm_scores(folder)
        subtask_scores.append((best_clip_scores, clip_scores, best_vlm_scores, vlm_scores))
    
    return aggregator_scores, subtask_scores

def calcstat_aggre_sub(aggregator_scores, subtask_scores):
    aggregator_best_clip_mean = []
    aggregator_clip_mean = []
    aggregator_best_vlm_mean = []
    aggregator_vlm_mean = []

    subtask_best_clip_mean = []
    subtask_clip_mean = []
    subtask_best_vlm_mean = []
    subtask_vlm_mean = []

    for best_clip_scores, clip_scores, best_vlm_scores, vlm_scores in aggregator_scores:
        aggregator_best_clip_mean.append(sum(best_clip_scores) / len(best_clip_scores))
        aggregator_clip_mean.append(sum(clip_scores) / len(clip_scores))
        aggregator_best_vlm_mean.append(sum(best_vlm_scores) / len(best_vlm_scores))
        aggregator_vlm_mean.append(sum(vlm_scores) / len(vlm_scores))

    for best_clip_scores, clip_scores, best_vlm_scores, vlm_scores in subtask_scores:
        subtask_best_clip_mean.append(sum(best_clip_scores) / len(best_clip_scores))
        subtask_clip_mean.append(sum(clip_scores) / len(clip_scores))
        subtask_best_vlm_mean.append(sum(best_vlm_scores) / len(best_vlm_scores))
        subtask_vlm_mean.append(sum(vlm_scores) / len(vlm_scores))

    return {
        "aggregator_best_clip_mean": sum(aggregator_best_clip_mean) / len(aggregator_best_clip_mean),
        "aggregator_clip_mean": sum(aggregator_clip_mean) / len(aggregator_clip_mean),
        "aggregator_best_vlm_mean": sum(aggregator_best_vlm_mean) / len(aggregator_best_vlm_mean),
        "aggregator_vlm_mean": sum(aggregator_vlm_mean) / len(aggregator_vlm_mean),
        "subtask_best_clip_mean": sum(subtask_best_clip_mean) / len(subtask_best_clip_mean),
        "subtask_clip_mean": sum(subtask_clip_mean) / len(subtask_clip_mean),
        "subtask_best_vlm_mean": sum(subtask_best_vlm_mean) / len(subtask_best_vlm_mean),
        "subtask_vlm_mean": sum(subtask_vlm_mean) / len(subtask_vlm_mean),
    }

def table_for_aggregator_subtask(aggregator_scores, subtask_scores):
    stat = calcstat_aggre_sub(aggregator_scores, subtask_scores)

    print("Category".ljust(15), "Clip".ljust(15), "VLM".ljust(15))
    print("Aggregator".ljust(15), 
          f"{stat['aggregator_best_clip_mean']:.2f}/{stat['aggregator_clip_mean']:.2f}".ljust(15), 
          f"{stat['aggregator_best_vlm_mean']:.2f}/{stat['aggregator_vlm_mean']:.2f}".ljust(15))
    print("Subtask".ljust(15), 
          f"{stat['subtask_best_clip_mean']:.2f}/{stat['subtask_clip_mean']:.2f}".ljust(15), 
          f"{stat['subtask_best_vlm_mean']:.2f}/{stat['subtask_vlm_mean']:.2f}".ljust(15))

if __name__ == "__main__":
    evaluated_datapaths = [
        "exp/eval_python_full_10x_shapes_daily_4omini",
        "exp/eval_python_single_10x_shapes_daily_4omini",
        "exp/eval_scad_full_3x_shapes_daily_multistruct_4omini",
        "exp/eval_scad_full_3x_shapes_primitive_multi_4omini",
        "exp/eval_scad_full_10x_shapes_daily_4omini",
        "exp/eval_scad_single_3x_shapes_daily_multistruct_4omini",
        "exp/eval_scad_single_3x_shapes_primitive_multi_4omini",
        "exp/eval_scad_single_10x_shapes_daily_4omini",        
    ]
    paths = [os.path.abspath(p) for p in evaluated_datapaths]
    test_path = [
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini"
    ]
    # full vs single
    # results = eval_paths(evaluated_datapaths)
    # table(results)

    # aggregator vs subtask
    aggregator_folders, subtask_folders = get_all_aggregator_and_subtask_folders(test_path[0])
    aggregator_scores, subtask_scores = eval_aggregator_vs_subtask(aggregator_folders, subtask_folders)
    table_for_aggregator_subtask(aggregator_scores, subtask_scores)

