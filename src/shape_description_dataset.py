from synset import synset_by_offset
import os
import json
import random
import shutil


def process_directory(directory):
    '''
    Process the directory to establish the mapping between category folder names and category names.
    '''
    results = {}
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            result = synset_by_offset(folder_name)
            results[folder_name] = result
    return results

def establish_category_mapping(directory):
    '''
    Process the directory to establish the mapping between category folder names and category names, and save the mapping to a JSON file.
    '''
    results = process_directory(directory)
    mapping_path = os.path.join(directory, 'category_mapping.json')
    with open(mapping_path, 'w') as f:
        json.dump(results, f, indent=4)

def trim_dataset(directory, num_to_keep=50):
    '''
    Trim the dataset to keep only a certain number of subfolders in each category.
    '''
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        if os.path.isdir(folder_path):
            subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
            if len(subfolders) > num_to_keep:
                subfolders_to_remove = random.sample(subfolders, len(subfolders) - num_to_keep)
                for subfolder in subfolders_to_remove:
                    shutil.rmtree(os.path.join(folder_path, subfolder))

if __name__ == "__main__":
    # establish_category_mapping('dataset/shapenetcore_select')
    # trim_dataset('dataset/shapenetcore_select')
    pass
