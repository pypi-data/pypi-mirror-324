import os
import tempfile
from unittest import mock

import boto3
import pytest
from moto import mock_aws

from ..config import get_config_from_aws_secret_manager, get_config_from_local_file, get_config_value, has_config_value


def test_has_config_value():
    assert not has_config_value('something')
    assert has_config_value('something', config={'something': 'asdf'})


def test_get_config_value():
    assert get_config_value('something', config={'something': 'asdf'}) == 'asdf'


def test_get_config_value_missing():
    """An error should be thrown when a setting is not present."""
    with pytest.raises(KeyError):
        assert get_config_value('something', config={}) == 'asdf'


def test_get_config_value_missing_default():
    """A default value can be used when a setting is missing."""
    assert get_config_value('something', config={}, default='asdf') == 'asdf'


def test_get_config_value_env_variable():
    """An environment variable should be used when available."""
    os.environ['SOMETHING'] = 'asdf'
    assert get_config_value('SOMETHING', config={}) == 'asdf'
    del os.environ['SOMETHING']


def test_get_config_value_env_variable_priority():
    """An environment variable should take priority over the config."""
    os.environ['SOMETHING'] = 'asdf'
    assert get_config_value('SOMETHING', config={'SOMETHING': 'lala'}) == 'asdf'
    del os.environ['SOMETHING']


@mock_aws
@pytest.mark.parametrize(
    ('secret_content', 'secret_decoded'),
    [
        ('{"my_key": "my_value"}', {"my_key": "my_value"}),
        ('{\n"my_key": "my_value"\n}', {"my_key": "my_value"}),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value"}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value",}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value",\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n# some comment\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n// some comment\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
    ],
)
def test_get_config_from_aws_secret_manager(secret_content, secret_decoded):
    boto3.client("secretsmanager").create_secret(Name="some_secret", SecretString=secret_content)

    config = get_config_from_aws_secret_manager("some_secret")

    assert isinstance(config, dict)
    assert config == secret_decoded


@pytest.mark.parametrize(
    ('secret_content', 'secret_decoded'),
    [
        ('{"my_key": "my_value"}', {"my_key": "my_value"}),
        ('{\n"my_key": "my_value"\n}', {"my_key": "my_value"}),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value"}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value",}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n"my_other_key": "my_other_value",\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n# some comment\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
        (
            '{\n"my_key": "my_value",\n// some comment\n"my_other_key": "my_other_value"\n}',
            {"my_key": "my_value", "my_other_key": "my_other_value"},
        ),
    ],
)
def test_get_config_from_local_file(secret_content, secret_decoded):
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        fp.write(secret_content.encode('utf-8'))
        fp.close()

        config = get_config_from_local_file(fp.name)

        assert isinstance(config, dict)
        assert config == secret_decoded


@pytest.fixture
def setenvvar(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {"my_other_key": "override"}
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield  # This is the magical bit which restore the environment after
