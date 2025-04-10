from datetime import datetime

from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str]


class DeviceORM(Base):
    __tablename__ = 'devices'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user: Mapped[int | None] = mapped_column(index=True)
    device_name: Mapped[str]
    created_at: Mapped[datetime]
    x: Mapped[float]
    y: Mapped[float]
    z: Mapped[float]
