import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EntryInput(BaseModel):
    word: str = Field(..., min_length=1, max_length=255, example="apple")
    translation: str = Field(..., min_length=1, example="яблоко")


class EntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    word: str
    translation: str
    created_at: datetime


class Error(BaseModel):
    error: str
