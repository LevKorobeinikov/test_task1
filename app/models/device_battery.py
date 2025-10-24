from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    func,
)
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class DeviceBattery(BaseModel):
    device_id = Column(
        Integer,
        ForeignKey('device.id', ondelete='CASCADE'),
        nullable=False,
    )
    battery_id = Column(
        Integer,
        ForeignKey('battery.id', ondelete='CASCADE'),
        nullable=False,
    )
    connected_at = Column(DateTime(timezone=True), server_default=func.now())
    device = relationship(
        'Device',
        back_populates='battery_connections',
        lazy='selectin',
    )
    battery = relationship(
        'Battery',
        back_populates='device_connections',
        lazy='selectin',
    )

    __table_args__ = (
        CheckConstraint(
            'device_id IS NOT NULL AND battery_id IS NOT NULL',
            name='device_battery_not_null',
        ),
    )
