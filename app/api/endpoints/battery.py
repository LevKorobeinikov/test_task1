from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import battery_crud
from app.schemas.battery import (
    BatteryCreate,
    BatteryRead,
    BatteryUpdate,
)

router = APIRouter()


@router.get(
    '/',
    response_model=list[BatteryRead],
    response_model_exclude_none=True,
)
async def get_batteries(
    session: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
):
    """Получить список батарей."""
    return await battery_crud.get_multi(session, skip=skip, limit=limit)


@router.get(
    '/{battery_id}',
    response_model=BatteryRead,
)
async def get_battery(
    battery_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Получить батарею по ID."""
    battery = await battery_crud.get(battery_id, session)
    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Battery not found',
        )
    return battery


@router.post(
    '/',
    response_model=BatteryRead,
    dependencies=[Depends(current_superuser)],
)
async def create_battery(
    battery_in: BatteryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создать новую батарею."""
    battery = await battery_crud.create(battery_in, session)
    return battery


@router.patch(
    '/{battery_id}',
    response_model=BatteryRead,
    dependencies=[Depends(current_superuser)],
)
async def update_battery(
    battery_id: int,
    battery_in: BatteryUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновить батарею."""
    battery = await battery_crud.get(battery_id, session)
    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Battery not found',
        )
    battery = await battery_crud.update(
        battery,
        battery_in,
        session,
    )
    return battery


@router.delete(
    '/{battery_id}',
    dependencies=[Depends(current_superuser)],
)
async def delete_battery(
    battery_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удалить батарею."""
    battery = await battery_crud.get(battery_id, session)
    if not battery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Battery not found',
        )
    await battery_crud.remove(battery, session)
    return {'detail': 'Battery deleted successfully'}
