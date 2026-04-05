import { useEffect, useMemo, useState } from 'react';

import ReservationForm, { emptyForm } from './components/ReservationForm';
import ReservationsList from './components/ReservationsList';
import { createReservation, getReservations, getRooms } from './services/api';

function App() {
  const [rooms, setRooms] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [message, setMessage] = useState('');

  const selectedRoom = useMemo(
    () => rooms.find((room) => String(room.id) === form.room_id),
    [rooms, form.room_id]
  );

  async function loadData() {
    const [roomsData, reservationsData] = await Promise.all([getRooms(), getReservations()]);
    setRooms(roomsData);
    setReservations(reservationsData);
  }

  useEffect(() => {
    loadData().catch((error) => setMessage(error.message));
  }, []);

  function onFormChange(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function onSubmit(event) {
    event.preventDefault();
    setMessage('');

    const payload = {
      ...form,
      room_id: Number(form.room_id),
      attendees: form.attendees
        .split(',')
        .map((email) => email.trim())
        .filter(Boolean)
    };

    try {
      await createReservation(payload);
      setForm(emptyForm);
      setMessage('Reserva creada correctamente.');
      await loadData();
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <main className="container">
      <h1>Mini LibreBooking</h1>
      <p>Arquitectura separada por módulos (API, servicios y componentes).</p>

      <ReservationForm
        rooms={rooms}
        form={form}
        onFormChange={onFormChange}
        onSubmit={onSubmit}
        selectedRoomName={selectedRoom?.location}
      />

      {message && <p className="message">{message}</p>}

      <ReservationsList reservations={reservations} />
    </main>
  );
}

export default App;
