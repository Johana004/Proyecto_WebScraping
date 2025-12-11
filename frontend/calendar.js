const API_BASE = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", async () => {
    try {
        const res = await fetch(`${API_BASE}/api/events`);
        const events = await res.json();

        const calendarEl = document.getElementById("calendar-root"); // FIX

        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: "dayGridMonth",
            events: events
        });

        calendar.render();
    } catch (error) {
        console.error("Error cargando eventos:", error);
    }
});
