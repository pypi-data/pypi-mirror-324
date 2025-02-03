import argparse
import json
import sys

from resumaker.config import config
from resumaker.utils import is_resume_obj_valid, common_fields
from resumaker.render_resume import *
from resumaker.templates.t1.resume import Resume
from resumaker.templates.t1.template import ResumeTemplate
from resumaker.__about__ import __version__


def main():
    parser = get_parser()

    args = parser.parse_args()

    resume_filenames = get_resume_filenames(args.filenames)

    # check if files exist
    complete_resume_obj, filename, errors = get_resume_obj(resume_filenames)
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    

    # check validity (schema) of resume common fields
    is_valid, err_msg = is_resume_obj_valid(complete_resume_obj, filename)
    if not is_valid:
        sys.exit(err_msg)

    common_sections = {
        "name": complete_resume_obj.get("name"),
        "location": complete_resume_obj.get("location"),
        "contact": complete_resume_obj.get("contact"),
        "education": complete_resume_obj.get("education"),
        "links": complete_resume_obj.get("links"),
    }

    all_targets = get_targets(args.target, complete_resume_obj, common_sections)

    template = ResumeTemplate("t1")

    for target in all_targets:
        resume = Resume(
            target,
            template,
            order=config.get("ORDER"),
        )
        resume.build(build_name(target))
        # print(json.dumps(complete_resume_obj, indent=2))


def build_name(target):
    user_name = target["name"].replace(" ", "").lower()
    target_name = target["target_name"]
    return f"{user_name}-{target_name}"


def get_resume_filenames(filenames_arg):
    resume_filenames = config["RESUME_FILENAME"]

    if filenames_arg:
        resume_filenames = filenames_arg
        if type(resume_filenames) != list:
            resume_filenames = [filenames_arg]

    return resume_filenames


def get_targets(target_args, complete_resume_obj, common_sections):
    user_specified_target = target_args if target_args else None
    user_given_targets = [
        key for key in complete_resume_obj.keys() if key not in common_fields
    ]

    all_targets = []
    if user_specified_target:
        if user_specified_target in user_given_targets:
            all_targets.append(
                complete_resume_obj[user_specified_target]
                | {"target_name": user_specified_target}
                | common_sections
            )
        else:
            sys.exit("Target is not in the resume")
    else:
        for target in user_given_targets:
            all_targets.append(
                complete_resume_obj[target] | {"target_name": target} | common_sections
            )

    return all_targets


def get_parser():
    parser = argparse.ArgumentParser(
        prog="resumaker",
        description="Build multi-profile ATS friendly resume from a single YAML file.",
        epilog="Thank you for using resumaker.\n"
        "To contribute, please visit https://github.com/sujaudd1n/resumaker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--filename",
        metavar="filename",
        dest="filenames",
        help="Filename of resume yaml file.",
    )
    parser.add_argument(
        "-t",
        "--target",
        metavar="target",
        dest="target",
        help="Select target such as devops or AI in your resume",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


if __name__ == "__main__":
    main()
