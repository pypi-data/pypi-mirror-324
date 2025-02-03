import pytest
from resumaker.render_resume import get_resume_obj


@pytest.fixture
def create_file(request):
    marker = request.node.get_closest_marker("fixture_data")
    if marker is not None:
        data = marker.args[0]
    else:
        data = None
    return data


class TestGetResumeObj:
    @pytest.mark.fixture_data(["file1.yml"])
    def test_filenames_does_not_exist(self, mocker, create_file):
        patch1 = mocker.patch("resumaker.render_resume.read_file_txt")
        patch1.side_effect = FileNotFoundError

        result, filename, error = get_resume_obj(create_file)
        assert result is None
        assert error is not None
        assert filename == None
        assert error[0] == "file1.yml is not found!"

    @pytest.mark.fixture_data(["file1.yml"])
    def test_filenames_exists_but_invalid(self, mocker, create_file):
        patch1 = mocker.patch("resumaker.render_resume.read_file_txt")
        patch1.return_value = "%sk lsdjf ls"

        patch1 = mocker.patch("resumaker.render_resume.render_yaml_txt")
        patch1.side_effect = SystemExit

        with pytest.raises(SystemExit):
            result,filename, error = get_resume_obj(create_file)

    @pytest.mark.fixture_data(["file1.yml"])
    def test_filenames_exists_and_valid(self, mocker, create_file):
        patch1 = mocker.patch("resumaker.render_resume.read_file_txt")
        patch1.return_value = "key: val"

        patch1 = mocker.patch("resumaker.render_resume.render_yaml_txt")
        patch1.return_value = {"key": "val"}

        result, filename,  error = get_resume_obj(create_file)
        assert result is not None
        assert error is None
        assert filename == "file1.yml"
        assert result == {"key": "val"}
