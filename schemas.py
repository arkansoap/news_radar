import datetime
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional, Union, Dict
import json


class NewsRadarXPostBase(BaseModel):
    username: str
    text: str
    link: str
    date: datetime.datetime


class YouTubeFeedEntryWrite(NewsRadarXPostBase):
    pass


class YouTubeFeedEntryRead(NewsRadarXPostBase):
    id: int

    class Config:
        from_attributes = True
