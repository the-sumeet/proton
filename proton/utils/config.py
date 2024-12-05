import json
from proton.schema.app_config import ProtonAppConfig

CONFIG_FILE_NAME = "proton.json"


def load_app_config(app_path: str) -> ProtonAppConfig:
    """
    Open the proton.json file in the `app_path` and load the configuration, return as dict.

    :param app_path: Path of the app
    :raises FileNotFoundError: If `app_path/proton.json` is not a valid path
    """

    config_json = json.load(open(f"{app_path}/{CONFIG_FILE_NAME}"))
    return ProtonAppConfig(**config_json)
