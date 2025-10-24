from app.crud.base import CRUDBase
from app.models.battery import Battery


class CRUDBattery(CRUDBase):
    pass


battery_crud = CRUDBattery(Battery)
