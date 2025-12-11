const API_BASE = "http://127.0.0.1:5000";

async function renderResults() {
    const container = document.getElementById("results");
    container.innerHTML = "Cargando productos...";

    const res = await fetch(`${API_BASE}/api/products`);
    const productos = await res.json();

    container.innerHTML = productos.length === 0
        ? "<p>No hay productos</p>"
        : productos
            .map(p => `
                <div class="card">
                    <h3>${p.titulo}</h3>
                    <p>Precio: ${p.precio}</p>
                    <p>URL: <a href="${p.url_origen}" target="_blank">Ver producto</a></p>
                </div>
            `)
            .join("");
}

document.addEventListener("DOMContentLoaded", renderResults);
