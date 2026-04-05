CREATE TABLE IF NOT EXISTS rooms (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) NOT NULL UNIQUE,
  capacity INTEGER NOT NULL,
  location VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS reservations (
  id SERIAL PRIMARY KEY,
  room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
  title VARCHAR(120) NOT NULL,
  organizer_email VARCHAR(120) NOT NULL,
  attendees VARCHAR(500) NOT NULL DEFAULT '',
  start_time TIMESTAMP NOT NULL,
  end_time TIMESTAMP NOT NULL,
  teams_url VARCHAR(800) NOT NULL,
  outlook_url VARCHAR(800) NOT NULL
);

INSERT INTO rooms (name, capacity, location)
VALUES
  ('Atenas', 6, 'Planta 1'),
  ('Berlín', 8, 'Planta 2'),
  ('Lisboa', 4, 'Planta 1')
ON CONFLICT (name) DO NOTHING;
