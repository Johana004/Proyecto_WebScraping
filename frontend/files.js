const API_BASE = "http://127.0.0.1:5000";

async function loadFiles() {
    const res = await fetch(`${API_BASE}/api/files`);
    const files = await res.json();

    const box = document.getElementById("files");
    box.innerHTML = files.length === 0
        ? "<p>No hay archivos</p>"
        : files.map(f => `
            <li>
                <a href="../downloads/${f.filename}" download>${f.filename}</a> 
                - Hash: ${f.hash}
            </li>
        `).join("");
}

document.addEventListener("DOMContentLoaded", loadFiles);
