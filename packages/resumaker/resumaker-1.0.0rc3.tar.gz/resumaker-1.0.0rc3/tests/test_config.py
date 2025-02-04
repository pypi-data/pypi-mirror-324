import os
import pytest
from resumaker.config import *
from resumaker.utils import *


@pytest.fixture
def delete_config_file():
    if os.path.exists("config.yml"):
        os.remove("config.yml")


@pytest.fixture
def create_invalid_config_file():
    open("config.yml", "w").close()
    yield
    os.remove("config.yml")


@pytest.fixture
def create_valid_config_file():
    f = open("config.yml", "w")
    f.write("key: value")
    f.close()
    yield
    os.remove("config.yml")


class TestGetConfig:
    def test_when_filenotfound(self, mocker):
        patch1 = mocker.patch("resumaker.config.read_file_txt")
        patch1.side_effect = FileNotFoundError
        config = get_config()
        assert config == default_configs

    def test_when_file_exists(self, mocker):
        patch1 = mocker.patch("resumaker.config.read_file_txt")
        patch1.return_value = "hello-world"

        return_obj = {"KEY": "val"}
        patch2 = mocker.patch("resumaker.config.manage_user_config_txt")
        patch2.return_value = return_obj

        config = get_config()
        assert config == return_obj


class TestManageUserConfigTxt:
    def test_when_config_obj_invalid(self, mocker, capsys):
        patch1 = mocker.patch("resumaker.config.render_yaml_txt")
        patch1.return_value = []
        patch2 = mocker.patch("resumaker.config.is_config_valid")
        patch2.return_value = False, "error"

        out = manage_user_config_txt(None)
        captured = capsys.readouterr()

        assert out == default_configs
        assert captured.out == "Warning: error. Using default configs.\n"

    def test_when_config_obj_valid(self, mocker):
        patch1 = mocker.patch("resumaker.config.render_yaml_txt")
        patch1.return_value = True
        patch2 = mocker.patch("resumaker.config.is_config_valid")
        patch2.return_value = True, None

        p3_return = {"KEY": "Merged with user config"}
        patch3 = mocker.patch("resumaker.config.merge_user_config_with_defaults")
        patch3.return_value = p3_return

        out = manage_user_config_txt(None)
        assert out == p3_return


@pytest.fixture
def apply_user_config_obj(request):
    marker = request.node.get_closest_marker("fixture_data")
    if marker is None:
        data = None
    else:
        data = marker.args[0]
    return data


class TestMergeUserConfigWithDefaults:
    @pytest.mark.fixture_data({})
    def test_when_not_overwritten(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == default_configs

    @pytest.mark.fixture_data({"RESUME_FILENAME": "custom.yml"})
    def test_when_overwritten_with_string(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config["RESUME_FILENAME"] == ["custom.yml"]

    @pytest.mark.fixture_data({"RESUME_FILENAME": ["custom.yml"]})
    def test_when_overwritten_with_list(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config["RESUME_FILENAME"] == ["custom.yml"]

    @pytest.mark.fixture_data({"custom_config": ["custom_value"]})
    def test_ignore_unsupported_config(self, apply_user_config_obj, mocker):
        config = merge_user_config_with_defaults(apply_user_config_obj)
        assert config == default_configs
