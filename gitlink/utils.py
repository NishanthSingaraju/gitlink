from contextlib import contextmanager
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from pathlib import Path
import random
import string
import tempfile
import os

def copy_tree_path(src: Path, dest: Path):
    return copy_tree(str(src), str(dest))

def copy_file_path(src: Path, dest: Path):
    return copy_file(str(src), str(dest))

def build_store_directory() -> Path:
    """Builds a directory under ~/.truss/models for the purpose of creating a Truss at."""
    rand_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    target_directory_path = Path(
        Path.home(), ".git_store", f"{rand_suffix}"
    )
    target_directory_path.mkdir(parents=True)
    return Path(target_directory_path)

def get_modified_time_of_file(file_path : Path):
    return os.path.getmtime(file_path)
    
@contextmanager
def given_or_temporary_dir(given_dir: Path = None):
    if given_dir is not None:
        yield given_dir
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

def flatten_dictionary(mapping):
    return {key: value for d in mapping for key, value in d.items()}