from pydantic import  BaseModel


class Method(BaseModel):
    name: str
    args: list[str]