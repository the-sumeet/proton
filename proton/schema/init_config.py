from pydantic import BaseModel, Field


class InitConfig(BaseModel):
    name: str = Field(...)
    fe_type: str = Field(...)
