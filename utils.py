import os

def get_path_folders_and_files(path):
    files = []
    folders = []
    
    for f in os.scandir(path):
        if f.is_dir():
            folders.append(f.name)
            
        else:
            files.append(f.name)
        
    
    return files, folders

