import sys
import subprocess
import os
import shutil
from pathlib import Path
from string import Template
from resumaker.template_str import template
from resumaker.config import config

BASE_DIR = config["BASE_DIR"]

ORDER = ["summary", "education", "skills", "work_experience", "projects", "links"]


class Resume:
    def __init__(
        self,
        values,
        template,
        /,
        order=ORDER,
    ):
        self.values = values
        self.template = template

        self.contact = Contact()
        self.summary = Summary()
        self.education = Education()
        self.skills = Skills()
        self.work_experience = WorkExperience()
        self.projects = Project()
        self.links = Links()

        self.setup_sections = [
            self.template.get_license(),
            self.template.get_preamble(),
            self.contact.generate_tex(
                self.template,
                self.values["contact"]
                | {"name": self.values["name"]}
                | {"location": self.values["location"]},
            ),
        ]

        # self.internal_sections = [self.summary, self.education, self.skills, self.links]
        self.internal_sections = order if order else ORDER

    def generate_tex(self):
        all_sections = []
        for section in self.setup_sections:
            all_sections.append(section)

        internal_sections = []
        for section in self.internal_sections:
            try:
                tex = getattr(self, section).generate_tex(
                self.template, self.values[section]
            )
            except:
                sys.exit(f"{section} is not valid for template.")
            
            internal_sections.append(tex)

        internal_tex_template = Template(template["main"])
        internal_tex_str = "\n".join(internal_sections)
        rendered_internal_tex = internal_tex_template.substitute(
            CONTENT=internal_tex_str
        )

        all_sections.append(rendered_internal_tex)

        return "\n".join(all_sections)

    def write_tex(self, filepath):
        with open(filepath, "w") as f:
            text = self.generate_tex()
            f.write(text)

    def build(self, filename):
        tex_filename = f"{filename}.tex"
        filepath = BASE_DIR.joinpath(
            f"templates/{self.template.get_template_name()}/{tex_filename}"
        )
        self.write_tex(filepath)

        old_cwd = os.getcwd()
        new_cwd = os.path.dirname(filepath)
        os.chdir(new_cwd)

        return_code = subprocess.run(
            ["pdflatex", "-interaction=batchmode", tex_filename]
            # ["pdflatex", tex_filename]
        )

        pdf_filename = f"{filename}.pdf"
        shutil.move(pdf_filename, os.path.join(old_cwd, pdf_filename))

        for ext in ["log", "out", "tex", "aux"]:
            os.remove(f"{filename}.{ext}")

        os.chdir(old_cwd)

    def __str__(self):
        return f"{self.name}"


class Contact:
    def generate_tex(self, template, values):
        return template.get_tex("contact", values)


class Summary:
    def generate_tex(self, template, values):
        return template.get_tex("summary", values)


class Education:
    def generate_tex(self, template, values):
        return template.get_tex("education", values)


class Links:
    def generate_tex(self, template, values):
        return template.get_tex("links", values)


class Skills:
    def generate_tex(self, template, values):
        return template.get_tex("skills", values)


class WorkExperience:
    def generate_tex(self, template, values):
        return template.get_tex("work_experience", values)


class Project:
    def generate_tex(self, template, values):
        return template.get_tex("projects", values)
