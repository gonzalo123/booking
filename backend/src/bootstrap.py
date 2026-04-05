from __future__ import annotations

from .db import SessionLocal, engine
from .models import Base
from .repositories.rooms_repository import RoomsRepository


def bootstrap() -> None:
    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        RoomsRepository(session).seed()
