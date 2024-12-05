from pydantic import BaseModel, Field


class ProtonAppConfig(BaseModel):
    fe_install: str = Field(alias="fe:install")
    fe_build: str = Field(alias="fe:build")
    fe_dev_watcher: str = Field(alias="fe:dev:watcher")
    fe_dev_serverurl: str = Field(alias="fe:dev:serverUrl")
