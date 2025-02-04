import sys
import os
import yaml
from pathlib import Path

from resumaker.utils import read_file_txt, render_yaml_txt, is_config_valid


def get_base_dir():
    path = Path(__file__).resolve().parent
    return path


CONFIG_FILENAME = "config.yml"
default_configs = {
    "RESUME_FILENAME": ["resume.yml", "resume.yaml"],
"ORDER" : ["summary", "education", "skills", "work_experience", "projects", "links"],
    "BASE_DIR": get_base_dir(),
}
BASE_DIR = get_base_dir()


def get_config():
    """
    Return config data by overwriting default_configs
    by reading config.yml if exists else default_configs
    """
    try:
        user_config_txt = read_file_txt(CONFIG_FILENAME)
    except FileNotFoundError:
        return default_configs
    else:
        return manage_user_config_txt(user_config_txt)


def manage_user_config_txt(user_config_txt):
    """
    if config_obj is valid, merge it with default_configs
    and return else return default_configs
    """
    user_config_obj = render_yaml_txt(user_config_txt)
    is_valid, err_msg = is_config_valid(user_config_obj)
    if is_valid:
        return merge_user_config_with_defaults(user_config_obj)
    else:
        print(f"Warning: {err_msg}. Using default configs.")
        return default_configs


def merge_user_config_with_defaults(user_config_obj):
    """
    Overwrite default_configs with user_config_obj.
    return default_config
    """
    for config in user_config_obj:
        if config in default_configs:
            user_config_value = user_config_obj[config]
            default_configs[config] = (
                user_config_value
                if type(user_config_value) == list
                else [user_config_value]
            )
        else:
            print(f"{config} is not supported!")
    return default_configs


config = get_config()
