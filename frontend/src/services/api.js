const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:5000';

async function parseJson(response) {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error ?? 'Error en la API');
  }
  return data;
}

export async function getRooms() {
  const response = await fetch(`${API_URL}/api/rooms`);
  return parseJson(response);
}

export async function getReservations() {
  const response = await fetch(`${API_URL}/api/reservations`);
  return parseJson(response);
}

export async function createReservation(payload) {
  const response = await fetch(`${API_URL}/api/reservations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return parseJson(response);
}
