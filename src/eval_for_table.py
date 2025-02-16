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

def table(result):
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

if __name__ == "__main__":
    evaluated_datapaths = [
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_single_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_full_10x_shapes_daily_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_daily_multistruct_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_3x_shapes_primitive_multi_4omini",
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_10x_shapes_daily_4omini",        
    ]
    test_path = [
        "C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_python_full_10x_shapes_daily_4omini"
    ]
    results = eval_paths(evaluated_datapaths)
    table(results)
