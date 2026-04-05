from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..models import Reservation, Room
from ..repositories.reservations_repository import ReservationsRepository
from ..repositories.rooms_repository import RoomsRepository
from .integrations import outlook_event_url, teams_meeting_url


class BookingError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class CreateReservationDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    room_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=120)
    organizer_email: str = Field(min_length=3, max_length=120)
    attendees: list[str] = Field(default_factory=list)
    start_time: datetime
    end_time: datetime


class BookingService:
    def __init__(self, rooms_repository: RoomsRepository, reservations_repository: ReservationsRepository) -> None:
        self.rooms_repository = rooms_repository
        self.reservations_repository = reservations_repository

    def list_rooms(self) -> list[Room]:
        return self.rooms_repository.list_rooms()

    def list_reservations(self) -> list[Reservation]:
        return self.reservations_repository.list_reservations()

    def create_reservation(self, dto: CreateReservationDTO) -> Reservation:
        if dto.start_time >= dto.end_time:
            raise BookingError("La hora de inicio debe ser anterior a la hora de fin")

        room = self.rooms_repository.get_by_id(dto.room_id)
        if room is None:
            raise BookingError("Sala no encontrada", status_code=404)

        conflicts = self.reservations_repository.find_conflicts(
            room_id=room.id,
            start_time=dto.start_time,
            end_time=dto.end_time,
        )
        if conflicts:
            raise BookingError("La sala ya está reservada en ese rango horario", status_code=409)

        reservation = Reservation(
            room_id=room.id,
            title=dto.title,
            organizer_email=dto.organizer_email,
            attendees=",".join(dto.attendees),
            start_time=dto.start_time,
            end_time=dto.end_time,
            teams_url=teams_meeting_url(dto.title, dto.start_time, dto.end_time),
            outlook_url=outlook_event_url(dto.title, dto.start_time, dto.end_time, room.location),
        )
        return self.reservations_repository.create(reservation)
