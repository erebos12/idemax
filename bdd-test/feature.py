from typing import Optional

from pydantic import BaseModel


class Feature:
    id: str
    filename: str
    content: str

    def __init__(self, id, filename, content):
        self.id = id
        self.filename = filename
        self.content = content


class FeatureRequest(BaseModel):
    id: Optional[str] = None
    filename: str
    content: str


# TODO make this work instead of returning artisan-crafted JSON string
class FeatureResponse(BaseModel):
    _id: str
    filename: str
    content: str
