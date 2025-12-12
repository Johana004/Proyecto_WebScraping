from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
import sys

# Permitir importar database.db desde carpeta principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(_file_))))

from database.db import get_connection

app = Flask(_name_)
CORS(app)


# ==========================
#   ENDPOINT: Productos (DB)
# ==========================
@app.get("/api/productos")
def get_productos():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, precio, url_origen, oferta, cantidad, estado_registro,
               hash_producto, version, last_seen, fecha_extraccion
        FROM productos
        ORDER BY id ASC;
    """)

    rows = cur.fetchall()

    data = []
    for r in rows:
        data.append({
            "id": r[0],
            "titulo": r[1],
            "precio": r[2],
            "url_origen": r[3],
            "oferta": r[4],
            "cantidad": r[5],
            "estado_registro": r[6],
            "hash_producto": r[7],
            "version": r[8],
            "last_seen": str(r[9]),
            "fecha_extraccion": str(r[10])
        })

    cur.close()
    conn.close()
    return jsonify(data)


# ==========================
#   ENDPOINT: JSON results
# ==========================
@app.get("/api/results")
def api_results():
    with open("data/results.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ==========================
#   ENDPOINT: JSON events
# ==========================
@app.get("/api/events")
def api_events():
    with open("data/events.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


# ==========================
#   ENDPOINT: JSON files
# ==========================
@app.get("/api/files")
def api_files():
    with open("data/files.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)


@app.get("/")
def home():
    return jsonify({"status": "API funcionando"})


if _name_ == "_main_":
    app.run(debug=True, port=5000)
