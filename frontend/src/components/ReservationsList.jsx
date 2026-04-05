function ReservationsList({ reservations }) {
  return (
    <section className="card">
      <h2>Reservas</h2>
      {reservations.length === 0 ? (
        <p>No hay reservas todavía.</p>
      ) : (
        <ul className="list">
          {reservations.map((reservation) => (
            <li key={reservation.id}>
              <h3>{reservation.title}</h3>
              <p>
                {reservation.room.name} · {reservation.room.location}
              </p>
              <p>
                {new Date(reservation.start_time).toLocaleString()} → {new Date(reservation.end_time).toLocaleString()}
              </p>
              <div className="links">
                <a href={reservation.teams_url} target="_blank" rel="noreferrer">
                  Crear en Teams
                </a>
                <a href={reservation.outlook_url} target="_blank" rel="noreferrer">
                  Abrir en Outlook
                </a>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default ReservationsList;
