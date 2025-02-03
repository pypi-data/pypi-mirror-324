# This file contains utilities to load config(s) from sources, e.g. a json file and environment variables

import os
from functools import cache
from pathlib import Path
from typing import Any

import boto3
import orjson
from google.cloud import secretmanager


def parse_bool(value: Any) -> bool:
    """Parse a value into a bool.

    Returns:
        The parsed boolean.
    """

    return str(value).lower() in {'true', '1', 'yes', 'on'}


def clean_lines_for_json_parsing(content: str) -> str:
    """Clean e.g. comments from the input so the input is json-parseable."""
    cleaned = ''.join(
        [l for l in content.split('\n') if not (l.strip().startswith('# ') or l.strip().startswith('// '))]  # noqa: E741
    )  # noqa: E741
    if cleaned.endswith(',}'):
        cleaned = cleaned.removesuffix(',}') + '}'
    return cleaned


def get_config_from_local_file(filename: str) -> dict:
    """Fetch the config by reading a local file.

    Returns:
        The config as a dictionary.
    """

    def try_find_relative_path(file_path: str, parent_path: Path | None = None) -> Path | None:
        """Traverse into parent directories to try and find a file in these directories when given a relative path."""

        # If its an absolute path, return that full path immediately
        if Path(file_path).is_absolute():
            return Path(file_path)

        # Start recursion from the path of this file itself
        if parent_path is None:
            return try_find_relative_path(file_path, Path(__file__).resolve(strict=True).parent)

        # If the file exists in this directory, return the full path to it.
        if Path(parent_path, file_path).exists():
            return Path(parent_path, file_path)

        # If we are at the root, then stop recursion
        if parent_path.parent == parent_path:
            return None

        # Try to move up one level
        return try_find_relative_path(file_path, Path(parent_path).parent)

    file_path = try_find_relative_path(filename)

    if not file_path:
        raise Exception('Specified local config file could not be found!')

    with file_path.open() as f:
        cleaned = clean_lines_for_json_parsing(f.read())
    return orjson.loads(cleaned.encode())


def get_config_from_aws_secret_manager(secret_name: str) -> dict:
    """Fetch config by reading secrets from AWS Secret Manager.

    The secret should contain json.

    Returns:
        The config as a dictionary.
    """

    payload = (
        boto3.session.Session()
        .client(service_name='secretsmanager')
        .get_secret_value(SecretId=secret_name)['SecretString']
    )
    cleaned = clean_lines_for_json_parsing(payload)
    return orjson.loads(cleaned.encode())


def get_config_from_google_secret_manager(secret_name: str) -> dict:
    """Fetch config by reading secrets from Google Secret Manager.

    The secret should contain json.

    Returns:
        The config as a dictionary
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise Exception('The environment variable GOOGLE_CLOUD_PROJECT must be set to a non-empty value!')

    payload = (
        secretmanager.SecretManagerServiceClient()
        .access_secret_version(name=f"projects/{project_id}/secrets/{secret_name}/versions/latest", timeout=5.0)
        .payload.data.decode("UTF-8")
    )

    cleaned = clean_lines_for_json_parsing(payload)

    return orjson.loads(cleaned.encode())


@cache
def load_config() -> dict:
    """Load the configuration based on an environment variable and return it as a dict.

    When multiple config sources are specified, each of them is loaded subsequently and its values can
    override values from the previous one(s). Last one wins.

    Returns:
        The loaded configuration as key/value dictionary.
    """

    config_source_list = [x for x in os.environ.get('CONFIG_SOURCE', '').split(';') if x]
    resulting_config = {'source': config_source_list}

    for config_source in config_source_list:
        config_source_type, config_location = config_source.split(':', 1)

        if config_source_type == 'file':
            resulting_config.update(get_config_from_local_file(config_location))
        elif config_source_type == 'gsm':
            resulting_config.update(get_config_from_google_secret_manager(config_location))
        elif config_source_type == 'asm':
            resulting_config.update(get_config_from_aws_secret_manager(config_location))
        else:
            raise Exception(f'Unkonwn config source declared: {config_source}')

    return resulting_config


def has_config_value(key: str, config: dict | None = None, **kwargs) -> bool:
    """Returns wether or not a certain setting is explicitly set in the config.

    If a key exists in the environment, use that instead of from the config, as we consider that an override with higher priority.

    This allows to do the behaviour of 'only set a certain setting if it is defined, otherwise use the default Django settings'
    """

    if parse_bool(kwargs.get('use_environment_variables', True)) and key in os.environ:
        return True

    if config is None:
        config = load_config()

    return key in config


def get_config_value(key: str, config: dict | None = None, **kwargs) -> Any:
    """Returns the value of a certain setting in the config.

    If a key exists in the environment, use that instead of from the config, as we consider that an override with higher priority.
    Optionally a default value can be given to use if a settings was not configured explicitly in the config.
    """

    if parse_bool(kwargs.get('use_environment_variables', True)) and key in os.environ:
        return os.environ[key]

    if config is None:
        config = load_config()

    if key in config:
        return config[key]

    if 'default' not in kwargs:
        raise Exception(f'Key "{key}" is not defined in the config ({config['source']}) and no default is given!')

    return kwargs['default']
