from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Battery(BaseModel):
    name = Column(String(100), index=True, nullable=False)
    nominal_voltage = Column(Float, nullable=False)
    residual_capacity = Column(Float, nullable=False)
    service_life = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    device_connections = relationship(
        'DeviceBattery',
        back_populates='battery',
        cascade='all, delete-orphan',
        lazy='selectin',
    )

    @property
    def devices(self):
        return [conn.device for conn in self.device_connections]

    def __repr__(self):
        base_repr = super().__repr__()
        return f'{base_repr}, {self.name=}'
