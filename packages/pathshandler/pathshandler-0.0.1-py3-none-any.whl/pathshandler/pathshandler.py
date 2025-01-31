import os
import json
from pathlib import Path
from typing import Optional

config_file = Path(__file__).parent / 'paths_config.json'


def load_config():
    """Load the paths_config.json file"""
    if config_file.exists():
        with open(config_file, "r") as f:
            return json.load(f)
        
    return {}


def save_config(config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)


def register_path(name: str, path: str):
    """Register a directory path with a given name."""

    config = load_config()
    config[name] = str(Path(path).resolve())
    save_config(config)
    print(f"Registered '{name}' -> {config[name]}")


def remove_path(name: str):
    """Remove a registered directory by name."""

    config = load_config()
    if name in config:
        del config[name]
        save_config(config)
        print(f"Removed '{name}' from registered paths.")
    else:
        print(f"No directory registered under '{name}'")


def get_path(name):
    """Retrieve the absolute path for a registered directory."""

    config = load_config()
    return config.get(name, None)



def search(name: str, pattern:Optional[str] = None, category:Optional[str] = "files", include_hidden:Optional[bool] = False):
    """Search for files or folders in the registered directory.

    Parameters
    ----------
    name : str
        Registered directory name.

    pattern : Optional[str], optional
        Pattern to search for. Defaults to None (returns all files/folders).

    category : Optional[str], optional
        'files', 'folders', or 'all'. Defaults to 'files'.

    include_hidden : Optional[bool], optional
        Whether to include hidden files/folders. Defaults to False.

    Returns
    -------
    list
        Matching file or folder paths.
    """
    


    directory = get_path(name)
    if not directory:
        print(f"No directory registered under '{name}'")
        return []
    
    path_obj = Path(directory)
    search_pattern = f"*{pattern}*" if pattern else "*"
    
    def is_hidden(p):
        return p.name.startswith(".") or any(part.startswith(".") for part in p.parts)
    
    def filter_results(paths):
        return [str(p) for p in paths if include_hidden or not is_hidden(p)]
    
    if category == "files":
        return filter_results(sorted([p for p in path_obj.rglob(search_pattern) if p.is_file()]))
    
    elif category == "folders":
        return filter_results(sorted([p for p in path_obj.rglob(search_pattern) if p.is_dir()]))
    
    elif category == "all":
        return filter_results(sorted(path_obj.rglob(search_pattern)))
    
    else:
        print("Invalid category. Choose from 'files', 'folders', or 'all'.")
        return []


