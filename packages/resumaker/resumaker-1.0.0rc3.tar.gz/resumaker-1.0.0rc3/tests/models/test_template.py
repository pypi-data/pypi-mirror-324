import pytest
from resumaker.templates.t1.template import *
from .tex_template import tex_template


class TestResumeTemplate:
    def test_template_import(self):
        resumeTemplate = ResumeTemplate("t1")
        template_dict = resumeTemplate.get_template_obj()
        assert type(template_dict) == dict


class TestContactTemplate:
    @pytest.fixture
    def contactObj(self):
        values = {
            "name": "test",
            "location": "location",
            "phone": "phone",
            "email": "email",
            "linkedin": "linkedin",
            "github": "github",
        }
        template = "$name$location$phone$email$linkedin$github"

        contactTemplate = ContactTemplate(template, values)
        return contactTemplate

    def test_render_tex(self, contactObj):
        tex = contactObj.render_tex()
        assert tex == "testlocationphoneemaillinkedingithub"


class TestSummaryTemplate:
    @pytest.fixture
    def summaryObj(self):
        values = {
            "title": "summary title",
            "text": "summary text",
        }
        template = "$title $text"

        summaryTemplate = SummaryTemplate(template, values)
        return summaryTemplate

    def test_render_tex(self, summaryObj):
        tex = summaryObj.render_tex()
        assert tex == "summary title summary text"


class TestEducationTemplate:
    @pytest.fixture
    def educationObj(self):
        values = [
            {
                "name": "CLGY",
                "location": "LOCX",
                "degree": "DEGZ",
                "duration": "DUR3",
                "achievements": ["A1", "A2", "A3"],
            },
            {
                "name": "CLGY2",
                "location": "LOCX2",
                "degree": "DEGZ2",
                "duration": "DUR32",
                "achievements": ["A12", "A22", "A32"],
            },
        ]
        template = {
            "complete": "S $all_educations E",
            "single": "$degree $duration $name $location $all_achievements",
            "achievement": "$achievement",
        }

        educationTemplate = EducationTemplate(template, values)
        return educationTemplate

    def test_render_tex(self, educationObj):
        tex = educationObj.render_tex()
        assert tex == (
            "S DEGZ DUR3 CLGY LOCX A1 A2 A3\nDEGZ2 DUR32 CLGY2 LOCX2 A12 A22 A32 E"
        )


class TestLinksTemplate:
    @pytest.fixture
    def linksObj(self):
        values = {
            "algorithms": [
                {
                    "name": "l1",
                    "url": "http://example.com/l1",
                    "url_text": "l1text",
                },
                {
                    "name": "l3",
                    "url": "http://example.com/l3",
                    "url_text": "l3text",
                },
            ],
            "open-source": [
                {
                    "name": "l2",
                    "url": "http://example.com/l2",
                    "url_text": "l2text",
                }
            ],
        }
        template = {
            "complete": "$all_links",
            "single": "$link_title $single_links",
            "single-link": "$link_url $link_url_text",
        }

        linksTemplate = LinksTemplate(template, values)
        return linksTemplate

    def test_render_tex(self, linksObj):
        tex = linksObj.render_tex()
        assert tex == (
            "Algorithms http://example.com/l1 l1text http://example.com/l3 l3text\n"
            "Open Source http://example.com/l2 l2text"
        )


class TestSkillsTemplate:
    @pytest.fixture
    def skillsObj(self):
        values = {
            "st1": ["s1", "s2"],
            "st2": ["s3"],
        }
        template = {
            "complete": "$all_skills",
            "single": "$skill_topic $skills_list",
        }

        skillsTemplate = SkillsTemplate(template, values)
        return skillsTemplate

    def test_render_tex(self, skillsObj):
        tex = skillsObj.render_tex()
        assert tex == ("St1 s1, s2\nSt2 s3")

    def test_format_skills_list(self, skillsObj):
        topic3 = [
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
            "WIDTH-1010",
        ]  # 12 total
        skills = skillsObj.format_skills_list(topic3)
        assert skills == (
            "WIDTH-1010, WIDTH-1010, WIDTH-1010, WIDTH-1010, "
            "WIDTH-1010, WIDTH-1010, WIDTH-1010, WIDTH-1010"
            " \\\\ &\n"
            "WIDTH-1010, WIDTH-1010, WIDTH-1010, WIDTH-1010"
        )


class TestWorkExperienceTemplate:
    @pytest.fixture
    def work_experience_obj(self):
        values = [
            {
                "company-name": "C1",
                "location": "L1",
                "role": "R1",
                "duration": "D1",
                "contributions": ["C1", "C2", "C3"],
            },
            {
                "company-name": "C2",
                "location": "L2",
                "role": "R2",
                "duration": "D2",
                "contributions": ["C4", "C5", "C6"],
            },
        ]
        template = {
            "complete": "$all_work_experiences",
            "single": "$company_name $location $role $duration $all_contributions",
            "single-contribution": "$contribution",
        }

        work_experience_template = WorkExperienceTemplate(template, values)
        return work_experience_template

    def test_render_tex(self, work_experience_obj):
        tex = work_experience_obj.render_tex()
        assert tex == ("C1 L1 R1 D1 C1\nC2\nC3\nC2 L2 R2 D2 C4\nC5\nC6")


class TestProjectTemplate:
    @pytest.fixture
    def project_obj(self):
        values = [
            {
                "name": "P1",
                "techstack": ["T1", "T2", "T3"],
                "details": ["D1", "D2", "D3"],
            },
            {
                "name": "P2",
                "techstack": ["T1", "T2", "T3"],
                "details": ["D1", "D2", "D3"],
            },
        ]
        template = {
            "complete": "$all_projects",
            "single": "$project_name $techstack $all_details",
            "single-detail": "$detail",
        }

        project_template = ProjectTemplate(template, values)
        return project_template

    def test_render_tex(self, project_obj):
        tex = project_obj.render_tex()
        assert tex == ("P1 T1, T2, T3 \nD1\nD2\nD3\n" "P2 T1, T2, T3 \nD1\nD2\nD3")
