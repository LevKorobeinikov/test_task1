from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Device(BaseModel):
    name = Column(String(100), unique=True, index=True, nullable=False)
    firmware_version = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    battery_connections = relationship(
        'DeviceBattery',
        back_populates='device',
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, {self.name=}'
