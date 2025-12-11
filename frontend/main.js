const API_BASE = "http://127.0.0.1:5000";

async function loadProducts() {
    const res = await fetch(`${API_BASE}/api/products`);
    const data = await res.json();
    console.log("Productos:", data);
}

async function loadFiles() {
    const res = await fetch(`${API_BASE}/api/files`);
    const data = await res.json();
    console.log("Archivos:", data);
}

async function loadEvents() {
    const res = await fetch(`${API_BASE}/api/events`);
    const data = await res.json();
    console.log("Eventos:", data);
}

document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    loadFiles();
    loadEvents();
});
