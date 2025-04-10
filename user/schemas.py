from pydantic import BaseModel, Field


class SRegister(BaseModel):
    username: str = Field(min_length=8)
