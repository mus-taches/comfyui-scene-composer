import os
import json
from glob import glob

ROOT_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..'))

DEFAULT_PATH = "config.default"
CUSTOM_PATH = "config"
VARIABLE_FILE = "variables.json"

RESERVED_KEYS = [
    "prefix",
    "suffix",
    "separator",
    "probability",
    "distribution",
    "number",
    "hide",
    "group_labels",
    "fixed"
]


def load_config(config_path="nodes", with_filename=True):
    "Load and merge config files"
    config_path = chose_config(config_path)
    config_files = glob(os.path.join(
        config_path, "**", "*.json"), recursive=True)

    config = {}
    for path in config_files:
        with open(path, 'r') as config_file:
            config_data = json.load(config_file)

            if with_filename:
                node_id = os.path.splitext(os.path.basename(path))[0]
                config[node_id] = config_data
            else:
                config = config_data

    return config


def chose_config(path=""):
    "Chose between default and custom config"
    custom_config_path = os.path.join(ROOT_PATH, CUSTOM_PATH)

    if os.path.exists(custom_config_path):
        folder_path = CUSTOM_PATH
    else:
        folder_path = DEFAULT_PATH

    absolute_config_path = os.path.join(ROOT_PATH, folder_path, path)

    return absolute_config_path
