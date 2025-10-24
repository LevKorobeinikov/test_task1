from fastapi import APIRouter

from app.api.endpoints import battery_router, device_router, user_router

main_router = APIRouter()

main_router.include_router(
    device_router,
    prefix='/devices',
    tags=['Devices'],
)

main_router.include_router(
    battery_router,
    prefix='/batteries',
    tags=['Batteries'],
)

main_router.include_router(user_router)
