import configparser
import os
from pathlib import Path
from datetime import datetime



project_path = Path(__file__).parent.parent


log_files = os.path.join(project_path, 'inputs/log_files.cfg')

def get_log_files(log_list):
    parser = configparser.ConfigParser()
    parser.read(log_files)
    get_version = parser.items( log_list)
    return get_version

def timestamp_name(prefix):
    """
    Creates timestamp
    Parameters: prefix (str):Name
    Returns:    name (str): timestamp
    """
    name = prefix + "_" + datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%f_%p")
    return name