from __future__ import annotations

import os

DATABASE_URL = os.getenv("BOOKING_DATABASE_URL", "sqlite:///booking.db")
HOST = os.getenv("BOOKING_HOST", "0.0.0.0")
PORT = int(os.getenv("BOOKING_PORT", "5000"))
DEBUG = os.getenv("BOOKING_DEBUG", "true").lower() == "true"
