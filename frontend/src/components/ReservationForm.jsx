const emptyForm = {
  room_id: '',
  title: '',
  organizer_email: '',
  attendees: '',
  start_time: '',
  end_time: ''
};

export { emptyForm };

function ReservationForm({ rooms, form, onFormChange, onSubmit, selectedRoomName }) {
  return (
    <section className="card">
      <h2>Nueva reserva</h2>
      <form onSubmit={onSubmit} className="form-grid">
        <label>
          Sala
          <select value={form.room_id} onChange={(event) => onFormChange('room_id', event.target.value)} required>
            <option value="">Selecciona una sala</option>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name} ({room.capacity} personas)
              </option>
            ))}
          </select>
        </label>

        <label>
          Título
          <input value={form.title} onChange={(event) => onFormChange('title', event.target.value)} required />
        </label>

        <label>
          Organizador
          <input
            type="email"
            value={form.organizer_email}
            onChange={(event) => onFormChange('organizer_email', event.target.value)}
            required
          />
        </label>

        <label>
          Asistentes (emails separados por coma)
          <input value={form.attendees} onChange={(event) => onFormChange('attendees', event.target.value)} />
        </label>

        <label>
          Inicio
          <input
            type="datetime-local"
            value={form.start_time}
            onChange={(event) => onFormChange('start_time', event.target.value)}
            required
          />
        </label>

        <label>
          Fin
          <input type="datetime-local" value={form.end_time} onChange={(event) => onFormChange('end_time', event.target.value)} required />
        </label>

        <button type="submit">Guardar reserva</button>
      </form>
      {selectedRoomName && (
        <small>
          Ubicación: <strong>{selectedRoomName}</strong>
        </small>
      )}
    </section>
  );
}

export default ReservationForm;
