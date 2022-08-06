from typing import Optional
from pydantic import BaseModel

class PostsSchema(BaseModel):
    desc: str
    image : Optional[str] = ""