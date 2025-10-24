from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.device import Device
from app.models.device_battery import DeviceBattery


class CRUDDevice(CRUDBase):
    async def get_batteries_count(
        self,
        device_id: int,
        session: AsyncSession,
    ) -> int:
        result = await session.execute(
            select(func.count(DeviceBattery.id)).where(
                DeviceBattery.device_id == device_id,
            ),
        )
        return result.scalar()

    async def can_add_battery(
        self,
        device_id: int,
        session: AsyncSession,
    ) -> bool:
        count = await self.get_batteries_count(device_id, session)
        return count < 5


device_crud = CRUDDevice(Device)
