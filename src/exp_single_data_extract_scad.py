import os
from pathlib import Path
from typing import List, Dict, NamedTuple
import json
from dataclasses import dataclass

@dataclass
class ShapeFiles:
    obj_files: List[Path]
    png_files: List[Path]
    scad_files: List[Path]
    log_files: List[Path]
    history_jsons: List[Path]
    eval_history_json: Path | None
    eval_prompt_md: Path | None
    evaluations_json: Path | None
    shape_description: Path | None
    shape_index: str
    
    def to_dict(self) -> Dict:
        """Convert the data to a dictionary format"""
        return {
            'shape_index': self.shape_index,
            'obj_files': [str(p) for p in self.obj_files],
            'png_files': [str(p) for p in self.png_files],
            'scad_files': [str(p) for p in self.scad_files],
            'log_files': [str(p) for p in self.log_files],
            'history_json': [str(p) for p in self.history_jsons],
            'eval_history_json': str(self.eval_history_json) if self.eval_history_json else None,
            'eval_prompt_md': str(self.eval_prompt_md) if self.eval_prompt_md else None,
            'evaluations_json': str(self.evaluations_json) if self.evaluations_json else None,
            'shape_description': str(self.shape_description) if self.shape_description else None
        }

class ShapeFolderCollector:
    def __init__(self, base_folder: str):
        """
        Initialize the collector with the base folder path.
        
        Args:
            base_folder (str): Path to the root folder containing shape_xxxx folders
        """
        self.base_folder = Path(base_folder)
        
    def get_shape_folders(self) -> List[Path]:
        """
        Get all shape folders matching the pattern shape_xxxx.
        
        Returns:
            List[Path]: List of paths to shape folders
        """
        pattern = "shape_[0-9][0-9][0-9][0-9]"
        return sorted(self.base_folder.glob(pattern))
    
    def collect_files_from_folder(self, shape_folder: Path) -> ShapeFiles:
        """
        Collect all relevant files from a single shape folder.
        
        Args:
            shape_folder (Path): Path to the shape folder
            
        Returns:
            ShapeFiles: Data structure containing all file information
        """
        history_files = []
        obj_files = []
        png_files = []
        scad_files = []
        log_files = []  # Added log files list
        
        # Get shape index from folder name
        shape_idx = shape_folder.name.split('_')[1]
        
        # Find all matching files
        for i in range(10):  # Assuming reasonable upper limit
            
            # {i}_history.json files
            history_file = shape_folder / f"{i}_history.json"
            if history_file.exists():
                history_files.append(history_file)
            
            for j in range(10):
                # Check if any matching files exist before continuing
                if not any(shape_folder.glob(f"{i}_{j}*")):
                    if j == 0:  # If no files found for this i, move to next i
                        break
                    continue  # If no more files for this j, move to next i
                
                # .obj files
                obj_file = shape_folder / f"{i}_{j}.obj"
                if obj_file.exists():
                    obj_files.append(obj_file)
                
                # .scad files
                scad_file = shape_folder / f"{i}_{j}.scad"
                if scad_file.exists():
                    scad_files.append(scad_file)
                
                # .log files
                log_file = shape_folder / f"{i}_{j}.log"
                if log_file.exists():
                    log_files.append(log_file)
                
                # .png files (including variations with k)
                for k in range(4):
                    png_file = shape_folder / f"{i}_{j}_{k}.png"
                    if png_file.exists():
                        png_files.append(png_file)
        
        # Single files
        eval_history = shape_folder / "evaluation_history.json"
        eval_prompt = shape_folder / "evaluation_prompt.md"
        evaluations = shape_folder / "evaluations.json"
        shape_desc = shape_folder / "shape_description.txt"
        
        return ShapeFiles(
            obj_files=sorted(obj_files),
            png_files=sorted(png_files),
            scad_files=sorted(scad_files),
            log_files=sorted(log_files),  # Added sorted log files
            history_jsons=sorted(history_files),
            eval_history_json=eval_history if eval_history.exists() else None,
            eval_prompt_md=eval_prompt if eval_prompt.exists() else None,
            evaluations_json=evaluations if evaluations.exists() else None,
            shape_description=shape_desc if shape_desc.exists() else None,
            shape_index=shape_idx
        )
    
    def collect_all_data(self) -> Dict[str, ShapeFiles]:
        """
        Collect data from all shape folders.
        
        Returns:
            Dict[str, ShapeFiles]: Dictionary mapping folder names to their file data
        """
        data = {}
        for shape_folder in self.get_shape_folders():
            data[shape_folder.name] = self.collect_files_from_folder(shape_folder)
        return data
    
    def get_data_as_dict(self) -> Dict[str, Dict]:
        """
        Get all data in a dictionary format suitable for JSON serialization.
        
        Returns:
            Dict[str, Dict]: Dictionary of all file data in JSON-serializable format
        """
        data = {}
        for folder_name, files in self.collect_all_data().items():
            data[folder_name] = files.to_dict()
        return data

def main():
    # Example usage
    collector = ShapeFolderCollector("C:\ZSY\imperial\courses\ISO\iso-shapecraft\exp\eval_scad_single_10x_shapes_daily_4omini")
    
    # Get structured data
    shape_data = collector.collect_all_data()
    
    # Example: Print all files for a shape
    for folder_name, files in shape_data.items():
        print(f"\nShape folder: {folder_name}")
        print("OBJ files:", [f.name for f in files.obj_files])
        print("PNG files:", [f.name for f in files.png_files])
        print("Log files:", [f.name for f in files.log_files])  # Added log files example
        print("Shape description:", files.shape_description)
        print("Evaluations:", files.evaluations_json)
        print("History:", [f.name for f in files.history_jsons])
    
    # Get data in dictionary format (suitable for JSON serialization)
    dict_data = collector.get_data_as_dict()
    
    # # Example: Save to JSON
    # with open('shape_data.json', 'w') as f:
    #     json.dump(dict_data, f, indent=2)

def get_shapefiles(folder_path: str) -> Dict[str, ShapeFiles]:
    collector = ShapeFolderCollector(folder_path)
    return collector.collect_all_data()

if __name__ == "__main__":
    main()