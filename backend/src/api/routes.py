from __future__ import annotations

from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session

from ..db import SessionLocal
from ..repositories.reservations_repository import ReservationsRepository
from ..repositories.rooms_repository import RoomsRepository
from ..services.booking import BookingError, BookingService, CreateReservationDTO
from .schemas import APIValidationError, parse_create_reservation, serialize_reservation, serialize_room

api_bp = Blueprint("api", __name__, url_prefix="/api")


def _build_service(session: Session) -> BookingService:
    return BookingService(
        rooms_repository=RoomsRepository(session),
        reservations_repository=ReservationsRepository(session),
    )


@api_bp.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@api_bp.get("/rooms")
def list_rooms():
    with SessionLocal() as session:
        service = _build_service(session)
        return jsonify([serialize_room(room) for room in service.list_rooms()])


@api_bp.get("/reservations")
def list_reservations():
    with SessionLocal() as session:
        service = _build_service(session)
        return jsonify([serialize_reservation(reservation) for reservation in service.list_reservations()])


@api_bp.post("/reservations")
def create_reservation():
    payload = request.get_json(silent=True) or {}

    try:
        request_model = parse_create_reservation(payload)
    except APIValidationError as error:
        return jsonify({"error": error.message}), 400

    dto = CreateReservationDTO(**request_model.model_dump())

    with SessionLocal() as session:
        service = _build_service(session)
        try:
            reservation = service.create_reservation(dto)
            return jsonify(serialize_reservation(reservation)), 201
        except BookingError as error:
            return jsonify({"error": error.message}), error.status_code
