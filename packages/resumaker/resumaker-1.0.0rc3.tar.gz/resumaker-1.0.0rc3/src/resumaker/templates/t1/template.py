import json
import os
from string import Template
from resumaker.config import BASE_DIR
from resumaker.utils import render_yaml_txt


class ResumeTemplate:
    "An interface between resume and actual template string."

    def __init__(self, name):
        self.name = name
        self.tex_template_obj = self.get_template_obj()

        self.contact = ContactTemplate
        self.summary = SummaryTemplate
        self.education = EducationTemplate
        self.skills = SkillsTemplate
        self.work_experience = WorkExperienceTemplate
        self.projects = ProjectTemplate
        self.links = LinksTemplate

    def get_template_name(self):
        return self.name

    def get_template_obj(self):
        with open(
            os.path.join(BASE_DIR, "templates", self.name, "tex_template.yml")
        ) as f:
            tex = f.read()

            tex_obj = render_yaml_txt(tex)
            return tex_obj

    def get_tex(self, section, values):
        return getattr(self, section)(
            self.tex_template_obj[section], values
        ).render_tex()

    def get_preamble(self):
        return self.tex_template_obj["preamble"]

    def get_license(self):
        return self.tex_template_obj["license"]


class ResumeSectionTemplate:
    def __init__(self, template, values):
        self.values = values
        self.template = template


class ContactTemplate(ResumeSectionTemplate):
    def render_tex(self):
        pyTemplate = Template(self.template)
        result = pyTemplate.substitute(
            name=self.values["name"],
            location=self.values["location"],
            phone=self.values["phone"],
            email=self.values["email"],
            linkedin=self.values["linkedin"],
            github=self.values["github"],
        )
        return result


class SummaryTemplate(ResumeSectionTemplate):
    def render_tex(self):
        pyTemplate = Template(self.template)
        result = pyTemplate.substitute(
            title=self.values["title"],
            text=self.values["text"],
        )
        return result


class EducationTemplate(ResumeSectionTemplate):
    def render_tex(self):
        py_complete_template = Template(self.template["complete"])
        py_single_template = Template(self.template["single"])
        py_achievement_template = Template(self.template["achievement"])

        rendered_single_educations = []
        for institute in self.values:
            rendered_achievements = []
            for achievement in institute["achievements"]:
                rendered_achievement = py_achievement_template.substitute(
                    achievement=achievement
                )
                rendered_achievements.append(rendered_achievement)
            rendered_single_education = py_single_template.substitute(
                name=institute["name"],
                duration=institute["duration"],
                degree=institute["degree"],
                location=institute["location"],
                all_achievements=" ".join(rendered_achievements),
            )
            rendered_single_educations.append(rendered_single_education)

        all_educations = "\n".join(rendered_single_educations)
        rendered_complete_education = py_complete_template.substitute(
            all_educations=all_educations
        )
        return rendered_complete_education


class LinksTemplate(ResumeSectionTemplate):
    def render_tex(self):
        py_complete_template = Template(self.template["complete"])
        py_single_template = Template(self.template["single"])
        py_single_link_template = Template(self.template["single-link"])

        rendered_links = []
        for link_category, link_lists in self.values.items():
            single_rendered_link = []
            for link in link_lists:
                single_rendered_link.append(
                    py_single_link_template.substitute(
                        link_url=link["url"], link_url_text=link["url_text"]
                    )
                )
            rendered_links.append(
                py_single_template.substitute(
                    link_title=" ".join(
                        list(
                            map(
                                lambda x: x[0].upper() + x[1:], link_category.split("-")
                            )
                        )
                    ),
                    single_links=" ".join(single_rendered_link),
                )
            )
        all_links = py_complete_template.substitute(all_links="\n".join(rendered_links))
        return all_links


class SkillsTemplate(ResumeSectionTemplate):
    def render_tex(self):
        complete_template = Template(self.template["complete"])
        single_template = Template(self.template["single"])
        rendered_skill_topics = []
        for skill_topic, skills_list in self.values.items():
            rendered_skill_topics.append(
                single_template.substitute(
                    skill_topic=skill_topic[0].upper() + skill_topic[1:],
                    skills_list=self.format_skills_list(skills_list),
                )
            )
        all_skills = complete_template.substitute(
            all_skills="\n".join(rendered_skill_topics)
        )
        return all_skills

    def format_skills_list(self, skills: list) -> str:
        line_width = -2
        lines = []
        line = []

        for skill in skills:
            if line_width + len(skill) > 100:
                lines.append(line[:])
                line = []
                line_width = -2
            line.append(skill)
            line_width += len(skill) + 2

        lines.append(line)
        lines = list(map(lambda x: ", ".join(x), lines))
        result = " \\\\ &\n".join(lines)
        return result


class WorkExperienceTemplate(ResumeSectionTemplate):
    def render_tex(self):
        complete_template = Template(self.template["complete"])
        single_template = Template(self.template["single"])
        contribution_template = Template(self.template["single-contribution"])

        rendered_single = []
        for experience in self.values:
            company_name = experience["company-name"]
            company_location = experience["location"]
            position = experience["role"]
            duration = experience["duration"]

            rendered_contributions = []
            for contribution in experience["contributions"]:
                rendered_contributions.append(
                    contribution_template.substitute(contribution=contribution)
                )

            rendered_single.append(
                single_template.substitute(
                    company_name=company_name,
                    location=company_location,
                    role=position,
                    duration=duration,
                    all_contributions="\n".join(rendered_contributions),
                )
            )

        all_experiences = complete_template.substitute(
            all_work_experiences="\n".join(rendered_single)
        )

        return all_experiences


class ProjectTemplate(ResumeSectionTemplate):
    def render_tex(self):
        complete_template = Template(self.template["complete"])
        single_template = Template(self.template["single"])
        detail_template = Template(self.template["single-detail"])

        rendered_single = []
        for project in self.values:
            project_name = project["name"]
            techstack = ", ".join(project["techstack"])

            rendered_details = []
            for detail in project["details"]:
                rendered_details.append(detail_template.substitute(detail=detail))

            rendered_single.append(
                single_template.substitute(
                    project_name=project_name,
                    techstack=techstack,
                    all_details="\n" + "\n".join(rendered_details),
                )
            )

        all_projects = complete_template.substitute(
            all_projects="\n".join(rendered_single)
        )

        return all_projects
