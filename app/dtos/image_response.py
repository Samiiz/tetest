from fastapi import UploadFile
from pydantic import BaseModel


class ImageResponse(BaseModel):
    file: UploadFile
    folder: str
    component: str
    target_id: int
    description: int
    url: str


class UrlResponse(BaseModel):
    url: str
