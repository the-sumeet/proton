from typing import Any

from pydantic import BaseModel, Field, model_validator


class InitConfig(BaseModel):
    name: str = Field(...)
    fe_type: str = Field(...)

    def fe_type_substitute(self) -> Any:
        return {
            self.fe_type: self.name,
        }
