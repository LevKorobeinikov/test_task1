from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BatteryBase(BaseModel):
    name: str
    nominal_voltage: float
    residual_capacity: float
    service_life: int


class BatteryCreate(BatteryBase):
    pass


class BatteryUpdate(BaseModel):
    name: Optional[str] = None
    nominal_voltage: Optional[float] = None
    residual_capacity: Optional[float] = None
    service_life: Optional[int] = None


class BatteryRead(BatteryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    devices: List['DeviceRead'] = []


class BatteryConnect(BaseModel):
    battery_id: int


class DeviceConnect(BaseModel):
    device_id: int
