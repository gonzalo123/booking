from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Room


class RoomsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_rooms(self) -> list[Room]:
        return self.session.scalars(select(Room).order_by(Room.name)).all()

    def get_by_id(self, room_id: int) -> Room | None:
        return self.session.get(Room, room_id)

    def seed(self) -> None:
        if self.session.scalar(select(Room.id)) is None:
            self.session.add_all(
                [
                    Room(name="Atenas", capacity=6, location="Planta 1"),
                    Room(name="Berlín", capacity=8, location="Planta 2"),
                    Room(name="Lisboa", capacity=4, location="Planta 1"),
                ]
            )
            self.session.commit()
