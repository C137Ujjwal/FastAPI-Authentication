# pretty much the pythonic version of the models with class with appropriate details
# it used pydantic

from pydantic import BaseModel


class PostBase(BaseModel):
    content: str
    title: str

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    class Config:
        orm_mode = True
