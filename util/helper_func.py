from typing import List 
import os 


def get_all_file_paths(folder_path: str) -> List[str]: 
    result = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        result.extend([os.path.join(dirpath, filename) for filename in filenames]) 
        
    return result 
