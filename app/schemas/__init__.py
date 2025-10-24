from .battery import (
    BatteryConnect,
    BatteryCreate,
    BatteryRead,
    BatteryUpdate,
    DeviceConnect,
)
from .device import DeviceCreate, DeviceRead, DeviceShort, DeviceUpdate
from .user import UserCreate, UserRead, UserUpdate

BatteryRead.model_rebuild()
DeviceRead.model_rebuild()

__all__ = [
    'UserRead',
    'UserCreate',
    'UserUpdate',
    'DeviceRead',
    'DeviceCreate',
    'DeviceUpdate',
    'DeviceShort',
    'BatteryRead',
    'BatteryCreate',
    'BatteryUpdate',
    'BatteryConnect',
    'DeviceConnect',
]
