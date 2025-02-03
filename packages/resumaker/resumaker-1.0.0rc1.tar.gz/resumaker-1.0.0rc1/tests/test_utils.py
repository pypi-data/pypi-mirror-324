import os
import pytest
from resumaker.utils import *


class TestReadFileTxt:
    @pytest.fixture
    def create_file(self, request):
        marker = request.node.get_closest_marker("create_file")
        if marker is None:
            data = None
        else:
            filename = marker.args[0]
            txt = marker.args[1]
        f = open(filename, "w")
        f.write(txt)
        f.close()
        yield
        os.remove(filename)

    @pytest.fixture
    def delete_file(self):
        if os.path.exists("file.txt"):
            os.remove("file.txt")

    def test_file_does_not_exist(self, delete_file):
        with pytest.raises(FileNotFoundError):
            read_file_txt("file.txt")

    @pytest.mark.create_file("file.txt", "")
    def test_file_exists_and_empty(self, create_file):
        txt = read_file_txt("file.txt")
        assert txt == ""

    @pytest.mark.create_file("file.txt", "hello-world")
    def test_file_exists_and_not_empty(self, create_file):
        txt = read_file_txt("file.txt")
        assert txt == "hello-world"


class TestIsConfigValid:
    def test_when_dict(self, mocker):
        config = is_config_valid({})
        assert config == (True, None)

    def test_when_list(self, mocker, capsys):
        config = is_config_valid([])
        assert config == (False, "config.yml should be convertible to Python dict")

    def test_when_value_is_dict(self, mocker, capsys):
        config = is_config_valid({"KEY": {}})
        assert config == (False, "Value of config has to be str or list of str")

    def test_when_value_is_list(self, mocker, capsys):
        config = is_config_valid({"KEY": []})
        assert config == (True, None)


class TestIsResumeValid:
    def test_when_dict(self, mocker):
        result = is_resume_obj_valid({}, "resume.yml")
        assert result == (False, "name does not exist in resume.yml")

    def test_when_some_fields_absent(self, mocker):
        result = is_resume_obj_valid(
            {
                "name": "test-user",
                "location": "location-y",
                "contact": {"phone": "9999999"},
                "education": [
                    {"name": "clg-1", "duration": "2222 - 3333", "degree": "deg360"}
                ],
            },
            "resume.yml",
        )
        assert result == (False, "links does not exist in resume.yml")


class TestCommonSectionContact:
    def test_valid(self):
        contact = {"name": "first last"}
        res = is_resume_contact_valid(contact)
        assert res == (True, None)

    def test_invalid(self):
        contact = {"name": ["first"]}
        with pytest.raises(AssertionError) as excinfo:
            res = is_resume_contact_valid(contact)
            assert excinfo.value == (False, "Value of contct.name should be a str")
    
    def test_invalid_key(self):
        contact = {"key": ["first"]}
        with pytest.raises(AssertionError) as excinfo:
            res = is_resume_contact_valid(contact)
            assert excinfo.value == (False, "key is not valid")


class TestCommonSectionEducation:
    def test_valid(self):
        education = [
            {
                "name": "clg",
                "location": "l",
                "duration": "x - y",
                "degree": "degA",
                "achievements": ["a1", "a2"],
            }
        ]
        res = is_resume_education_valid(education)
        assert res == (True, None)

        def test_invalid(self):

            education = [{
            'name': 'clg',
            'location': 'l',
            'duration': 'x - y',
            'degree': "degA",
            'achievements': ['a1', 'a2']
        }]
        res = is_resume_education_valid(education)
        assert res == (True, None)
