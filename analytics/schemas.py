from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SOnNameAllDevice(BaseModel):
    username: str


class SOnNameOneDevice(SOnNameAllDevice):
    device_name: str


class SCalculateAllTime(BaseModel):
    device_name: str


class SStats(BaseModel):
    device_name: str
    user: Optional[str] = None
    x: float
    y: float
    z: float


class SCalculateInterval(BaseModel):
    device_name: str
    start: datetime
    end: datetime
