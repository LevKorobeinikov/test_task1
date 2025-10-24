from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class DeviceBase(BaseModel):
    name: str
    firmware_version: str
    is_active: bool = True


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    firmware_version: Optional[str] = None
    is_active: Optional[bool] = None


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    batteries: List['BatteryRead'] = []


class DeviceShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    firmware_version: str
    is_active: bool
    batteries_count: int
    created_at: datetime
