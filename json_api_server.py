from flask import Flask, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_folder="../frontend", static_url_path="")

DATA_DIR = os.path.abspath("../data")

# ------------------------------
#   API: Productos
# ------------------------------
@app.get("/api/products")
def api_products():
    with open(os.path.join(DATA_DIR, "results.json"), "r", encoding="utf8") as f:
        data = json.load(f)
    return jsonify(data)

# ------------------------------
#   API: Eventos
# ------------------------------
@app.get("/api/events")
def api_events():
    with open(os.path.join(DATA_DIR, "events.json"), "r", encoding="utf8") as f:
        data = json.load(f)
    return jsonify(data)

# ------------------------------
#   API: Archivos
# ------------------------------
@app.get("/api/files")
def api_files():
    files_path = os.path.join(DATA_DIR, "files.json")
    if not os.path.exists(files_path):
        return jsonify([])
    with open(files_path, "r", encoding="utf8") as f:
        data = json.load(f)
    return jsonify(data)

# ------------------------------
#   Frontend: archivos estáticos
# ------------------------------
@app.get("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# rutas JS/CSS/imágenes
@app.get("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# ------------------------------
# Run server
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
