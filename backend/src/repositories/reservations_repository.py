from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Reservation


class ReservationsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_reservations(self) -> list[Reservation]:
        return self.session.scalars(select(Reservation).order_by(Reservation.start_time)).all()

    def find_conflicts(self, room_id: int, start_time: datetime, end_time: datetime) -> list[Reservation]:
        return self.session.scalars(
            select(Reservation)
            .where(Reservation.room_id == room_id)
            .where(Reservation.start_time < end_time)
            .where(Reservation.end_time > start_time)
        ).all()

    def create(self, reservation: Reservation) -> Reservation:
        self.session.add(reservation)
        self.session.commit()
        self.session.refresh(reservation)
        return reservation
