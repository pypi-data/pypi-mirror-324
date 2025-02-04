import yaml
import sys
from .utils import (
    read_file_txt,
    render_yaml_txt,
)


def get_resume_obj(filenames):
    """
    Return resume dict by rendering first successful filename
    """
    error_messages = []
    for filename in filenames:
        try:
            resume_yaml_txt = read_file_txt(filename)
        except FileNotFoundError:
            error_messages.append(f"{filename} is not found!")
            continue
        resume_obj = render_yaml_txt(resume_yaml_txt)
        return resume_obj, filename, None
    return None, None, error_messages
