# Mini LibreBooking (Flask + React)

Clon mínimo para reservar salas de reuniones con enlaces a Teams y Outlook, siguiendo una estructura modular inspirada en proyectos recientes de Gonzalo Ayuso (separación por capas: API, servicios y repositorios).

## Arquitectura

### Backend (`backend/`)

```text
backend
├── app.py                # entrypoint de compatibilidad
├── main.py               # entrypoint principal
└── src
    ├── app.py            # create_app + registro de blueprints
    ├── bootstrap.py      # creación de tablas + seed
    ├── db.py             # engine y session factory
    ├── models.py         # entidades SQLAlchemy
    ├── settings.py       # configuración por entorno
    ├── api
    │   ├── routes.py     # capa HTTP (Flask Blueprint)
    │   └── schemas.py    # serialización/parsing
    ├── repositories
    │   ├── rooms_repository.py
    │   └── reservations_repository.py
    └── services
        ├── booking.py    # reglas de negocio
        └── integrations.py
```

### Frontend (`frontend/`)

```text
frontend/src
├── App.jsx
├── components
│   ├── ReservationForm.jsx
│   └── ReservationsList.jsx
└── services
    └── api.js
```


## Convenciones

- Validación de entrada y DTOs con **Pydantic** (sin `dataclass`).
- Tipado explícito en repositorios, servicios y capa API.


## PostgreSQL local (Docker Compose)

Se incluye `composer.yml` con un servicio PostgreSQL que crea tablas y seed inicial mediante `deploy/postgres/init.sql`.

```bash
docker compose -f composer.yml up -d
```

Cadena de conexión para el backend:

```bash
export BOOKING_DATABASE_URL=postgresql+psycopg2://booking:booking@localhost:5432/booking
```

> Nota: cuando lo migres a RDS solo tendrás que cambiar `BOOKING_DATABASE_URL`.

## Ejecutar backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Servidor API en `http://localhost:5000`.

## Ejecutar frontend

```bash
cd frontend
npm install
npm run dev
```

Aplicación web en `http://localhost:5173`.

## Endpoints API

- `GET /api/health`
- `GET /api/rooms`
- `GET /api/reservations`
- `POST /api/reservations`

Ejemplo de payload:

```json
{
  "room_id": 1,
  "title": "Planificación Sprint",
  "organizer_email": "pm@empresa.com",
  "attendees": ["dev1@empresa.com", "dev2@empresa.com"],
  "start_time": "2026-04-05T10:00:00",
  "end_time": "2026-04-05T11:00:00"
}
```

## Nota sobre integración Teams/Outlook

Actualmente usa deep links. El siguiente paso sería OAuth + Microsoft Graph para crear eventos/reuniones reales en nombre del usuario.
