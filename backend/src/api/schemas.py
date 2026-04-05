from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from ..models import Reservation, Room


class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    location: str


class ReservationRoomResponse(BaseModel):
    id: int
    name: str
    location: str


class ReservationResponse(BaseModel):
    id: int
    room: ReservationRoomResponse
    title: str
    organizer_email: str
    attendees: list[str]
    start_time: datetime
    end_time: datetime
    teams_url: str
    outlook_url: str


class CreateReservationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    room_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=120)
    organizer_email: str = Field(min_length=3, max_length=120)
    attendees: list[str] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime


class APIValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def parse_create_reservation(payload: dict[str, object]) -> CreateReservationRequest:
    try:
        return CreateReservationRequest.model_validate(payload)
    except ValidationError as exc:
        errors = "; ".join(
            f"{'.'.join(str(value) for value in error['loc'])}: {error['msg']}" for error in exc.errors()
        )
        raise APIValidationError(errors) from exc


def serialize_room(room: Room) -> dict[str, object]:
    return RoomResponse(
        id=room.id,
        name=room.name,
        capacity=room.capacity,
        location=room.location,
    ).model_dump()


def serialize_reservation(reservation: Reservation) -> dict[str, object]:
    return ReservationResponse(
        id=reservation.id,
        room=ReservationRoomResponse(
            id=reservation.room.id,
            name=reservation.room.name,
            location=reservation.room.location,
        ),
        title=reservation.title,
        organizer_email=reservation.organizer_email,
        attendees=reservation.attendees.split(",") if reservation.attendees else [],
        start_time=reservation.start_time,
        end_time=reservation.end_time,
        teams_url=reservation.teams_url,
        outlook_url=reservation.outlook_url,
    ).model_dump(mode="json")
