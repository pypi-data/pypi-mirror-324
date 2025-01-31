from pathlib import Path

def get_project_root() -> Path:
    """Returns the path to the project root folder.
    Returns:
        The path to the project root folder.
    """
def get_data_path() -> Path:
    """Returns the path to the dataset cache ([root] / data)
    Returns:
        The path to the dataset cache
    """
def cache_file(file_name: str, url: str) -> Path:
    """Check if file_name already is in the data path, otherwise download it from url.
    Args:
        file_name: the file name
        url: the URL of the dataset
    Returns:
        The relative path to the dataset
    """
