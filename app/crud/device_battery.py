from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.battery import Battery
from app.models.device import Device
from app.models.device_battery import DeviceBattery


class CRUDDeviceBattery:
    async def create_connection(
        self,
        session: AsyncSession,
        device_id: int,
        battery_id: int,
    ):
        device_result = await session.execute(
            select(Device).where(Device.id == device_id),
        )
        device = device_result.scalars().first()
        if not device:
            raise ValueError('Device not found')
        battery_result = await session.execute(
            select(Battery).where(Battery.id == battery_id),
        )
        if not battery_result.scalars().first():
            raise ValueError('Battery not found')
        existing_result = await session.execute(
            select(DeviceBattery).where(
                and_(
                    DeviceBattery.device_id == device_id,
                    DeviceBattery.battery_id == battery_id,
                ),
            ),
        )
        if existing_result.scalars().first():
            raise ValueError('Connection already exists')
        connection = DeviceBattery(
            device_id=device_id,
            battery_id=battery_id,
        )
        session.add(connection)
        await session.commit()
        await session.refresh(connection)
        return connection

    async def delete_connection(
        self,
        session: AsyncSession,
        device_id: int,
        battery_id: int,
    ):
        result = await session.execute(
            select(DeviceBattery).where(
                and_(
                    DeviceBattery.device_id == device_id,
                    DeviceBattery.battery_id == battery_id,
                ),
            ),
        )
        connection = result.scalars().first()
        if connection:
            await session.delete(connection)
            await session.commit()
            return True
        return False


device_battery_crud = CRUDDeviceBattery()
