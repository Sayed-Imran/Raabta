from typing import Optional
from pydantic import BaseModel

class PostsSchema(BaseModel):
    post_title: str
    post_content: str
    published: bool = True
    image : Optional[str] = ""
    likes : Optional[list] = []