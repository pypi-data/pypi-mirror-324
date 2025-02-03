import sys
import os
import yaml

common_fields = {
    "name": str,
    "location": str,
    "contact": dict,
    "education": list,
    "links": dict,
    "skills": dict,
}


def read_file_txt(filename):
    """Read filename and return its text"""
    with open(filename) as f:
        return f.read()


def render_yaml_txt(yaml_txt):
    "Render and return yaml_txt"
    try:
        return yaml.safe_load(yaml_txt)
    except Exception as exc:
        sys.exit("Error: Coult not parse yaml: " + str(exc))


def is_resume_obj_valid(resume_obj, filename):
    def check(field, dtype, dtype_msg):
        assert resume_obj.get(field), f"{field} does not exist in {filename}"
        assert isinstance(
            resume_obj.get(field), dtype
        ), f"{field} should be {dtype_msg}"

    try:
        assert isinstance(resume_obj, dict), f"{filename} should be key-value pair"

        check("name", str, "a str")
        check("contact", dict, "a dictionary")
        check("education", list, "a list of dictionary")
        check("links", dict, "a dictionary")

        is_resume_contact_valid(resume_obj.get("contact"))
        is_resume_education_valid(resume_obj.get("education"))

    except AssertionError as exc:
        return False, str(exc)
    else:
        return True, None


def is_resume_contact_valid(contact):
    valid_keys = ["name", "location", "email", "phone", "linkedin", "github"]
    for key, val in contact.items():
        assert key in valid_keys, f"{key} is not valid for contact"
        assert type(val) == str, f"Value of contact.{key} should be a str"
    return True, None


def is_resume_education_valid(education_list):
    for education in education_list:
        assert type(education) == dict, "Education entry should be a dictionary"
        for key, val in education.items():
            if key == "achievements":
                assert (
                    type(education[key]) == list
                ), f"Value of education.<entry>.{key} should be a list"
                for achievement in education[key]:
                    print(achievement)
                    assert (
                        type(achievement) == str
                    ), f"Value of education.<entry>.{key}.<item> should be a str"
            else:
                assert (
                    type(val) == str
                ), f"Value of education.<entry>.{key} should be a str"
    return True, None


def is_config_valid(config_obj):
    """
    config_obj has to be a dict.
    Each value in key: value has to be a str or list
    """
    try:
        assert isinstance(
            config_obj, dict
        ), "config.yml should be convertible to Python dict"
        for _, val in config_obj.items():
            assert isinstance(val, list) or isinstance(
                val, str
            ), "Value of config has to be str or list of str"
    except AssertionError as exc:
        return False, str(exc)
    return True, None
