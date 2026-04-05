from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    capacity: Mapped[int]
    location: Mapped[str] = mapped_column(String(120))


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    title: Mapped[str] = mapped_column(String(120))
    organizer_email: Mapped[str] = mapped_column(String(120))
    attendees: Mapped[str] = mapped_column(String(500), default="")
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    teams_url: Mapped[str] = mapped_column(String(800))
    outlook_url: Mapped[str] = mapped_column(String(800))

    room: Mapped[Room] = relationship()
