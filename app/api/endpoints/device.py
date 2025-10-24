from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import device_battery_crud, device_crud
from app.schemas.battery import BatteryConnect
from app.schemas.device import (
    DeviceCreate,
    DeviceRead,
    DeviceShort,
    DeviceUpdate,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[DeviceShort],
    response_model_exclude_none=True,
)
async def get_devices(
    session: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
):
    """Получить список устройств."""
    devices = await device_crud.get_multi(session, skip=skip, limit=limit)
    result = []
    for device in devices:
        batteries_count = await device_crud.get_batteries_count(
            device.id,
            session,
        )
        result.append(
            DeviceShort(
                id=device.id,
                name=device.name,
                firmware_version=device.firmware_version,
                is_active=device.is_active,
                batteries_count=batteries_count,
                created_at=device.created_at,
            ),
        )
    return result


@router.get(
    '/{device_id}',
    response_model=DeviceRead,
)
async def get_device(
    device_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получить устройство по ID."""
    device = await device_crud.get(device_id, session)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Device not found',
        )
    return device


@router.post(
    '/',
    response_model=DeviceRead,
    dependencies=[Depends(current_superuser)],
)
async def create_device(
    device_in: DeviceCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новое устройство."""
    device = await device_crud.create(device_in, session)
    return device


@router.patch(
    '/{device_id}',
    response_model=DeviceRead,
    dependencies=[Depends(current_superuser)],
)
async def update_device(
    device_id: int,
    device_in: DeviceUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновить устройство."""
    device = await device_crud.get(device_id, session)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Device not found',
        )
    device = await device_crud.update(device, device_in, session)
    return device


@router.delete(
    '/{device_id}',
    dependencies=[Depends(current_superuser)],
)
async def delete_device(
    device_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить устройство."""
    device = await device_crud.get(device_id, session)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Device not found',
        )
    await device_crud.remove(device, session)
    return {'detail': 'Device deleted successfully'}


@router.post(
    '/{device_id}/batteries',
    dependencies=[Depends(current_superuser)],
)
async def connect_battery_to_device(
    device_id: int,
    battery_connect: BatteryConnect,
    session: AsyncSession = Depends(get_async_session),
):
    """Подключить батарею к устройству."""
    can_add = await device_crud.can_add_battery(device_id, session)
    if not can_add:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Device cannot have more than 5 batteries',
        )
    try:
        await device_battery_crud.create_connection(
            session,
            device_id,
            battery_connect.battery_id,
        )
        return {'detail': 'Battery connected successfully'}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    '/{device_id}/batteries/{battery_id}',
    dependencies=[Depends(current_superuser)],
)
async def disconnect_battery_from_device(
    device_id: int,
    battery_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Отключить батарею от устройства."""
    success = await device_battery_crud.delete_connection(
        session,
        device_id,
        battery_id,
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Connection not found',
        )
    return {'detail': 'Battery disconnected successfully'}
