import os
import json
from datetime import datetime
from database.db import get_connection


DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

RESULTS_JSON = os.path.join(DATA_DIR, "results.json")
EVENTS_JSON = os.path.join(DATA_DIR, "events.json")


def generar_results_json():
    """Genera results.json con todos los productos de la BD."""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, precio, url_origen, oferta, cantidad, estado_registro,
               hash_producto, version, last_seen, created_at
        FROM productos
        ORDER BY id ASC;
    """)

    rows = cur.fetchall()
    conn.close()

    productos = []
    for r in rows:
        productos.append({
            "id": r[0],
            "titulo": r[1],
            "precio": float(r[2]) if r[2] is not None else None,
            "url_origen": r[3],
            "oferta": r[4],
            "cantidad": r[5],
            "estado_registro": r[6],
            "hash_producto": r[7],
            "version": r[8],
            "last_seen": r[9].isoformat() if r[9] else None,
            "created_at": r[10].isoformat() if r[10] else None
        })

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

    print(f"[OK] Archivo generado: {RESULTS_JSON}")


def generar_events_json():
    """Genera events.json con eventos para el calendario FullCalendar."""

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, estado_registro, last_seen
        FROM productos
    """)

    rows = cur.fetchall()
    conn.close()

    eventos = []

    for r in rows:
        estado = r[2]
        color = "#3788d8"  # azul por defecto

        if estado == "Nuevo":
            color = "#28a745"  # verde
        elif estado == "Modificado":
            color = "#ffc107"  # amarillo
        elif estado == "Eliminado":
            color = "#dc3545"  # rojo

        eventos.append({
            "id": r[0],
            "title": f"{estado}: {r[1]}",
            "start": r[3].isoformat() if r[3] else datetime.now().isoformat(),
            "color": color
        })

    with open(EVENTS_JSON, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)

    print(f"[OK] Archivo generado: {EVENTS_JSON}")

def generar_files_json():
    path = os.path.join(DATA_FOLDER, "files.json")

    # Si no tienes archivos todavía, crea un array vacío
    archivos = []

    with open(path, "w", encoding="utf-8") as f:
        json.dump(archivos, f, indent=4, ensure_ascii=False)

    print("[OK] Archivo generado:", path)




def generar_todos():
    generar_results_json()
    generar_events_json()
    generar_files_json()
    print("\n[OK] Todos los JSON generados correctamente.\n")


if __name__ == "__main__":
    generar_todos()
