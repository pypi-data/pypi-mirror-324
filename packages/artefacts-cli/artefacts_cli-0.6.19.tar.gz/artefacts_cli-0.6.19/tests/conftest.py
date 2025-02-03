import pytest

import os

from click.testing import CliRunner

from tests.utils import docker_mock


def dockerfile_presence(mocker, value: bool):
    original = os.path.exists

    def exists(path):
        if "dockerfile" in path.lower():
            return value
        else:
            return original(path)

    return mocker.patch("os.path.exists", side_effect=exists, autospec=True)


@pytest.fixture(scope="function")
def dockerfile_available(mocker):
    return dockerfile_presence(mocker, True)


@pytest.fixture(scope="function")
def dockerfile_not_available(mocker):
    return dockerfile_presence(mocker, False)


@pytest.fixture(scope="module")
def docker_mocker(module_mocker):
    test_client = docker_mock.make_fake_api_client()
    module_mocker.patch("docker.APIClient", return_value=test_client)
    return test_client


@pytest.fixture(scope="module")
def cli_runner():
    return CliRunner()
