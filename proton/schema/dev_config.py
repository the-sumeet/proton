from pydantic import BaseModel

from proton.schema.app_config import ProtonAppConfig


class DevConfig(BaseModel):
    app_config: ProtonAppConfig
