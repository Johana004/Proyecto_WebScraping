# test_upsert.py
import json
import hashlib
from database.db import upsert_producto

def hash_texto(value: str):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

with open("productos_laptops.json", "r", encoding="utf-8") as f:
    productos = json.load(f)

for p in productos:
    # limpiar precio
    precio = None
    if p.get("precio") and isinstance(p.get("precio"), str):
        raw = p["precio"].replace("CRC", "").replace("$", "").replace(",", "").strip()
        try:
            precio = float(raw)
        except:
            precio = None
    else:
        precio = p.get("precio")

    # Obtener valores seguros
    titulo = p.get("titulo") or "Sin titulo"
    url = p.get("url") or "sin_url"
    precio_str = str(precio) if precio is not None else "sin_precio"

    # Crear hash seguro
    hash_producto = hash_texto(f"{titulo}-{url}-{precio_str}")

    producto = {
        "titulo": titulo,
        "precio": precio,
        "url_origen": url,
        "oferta": False,
        "cantidad": None,
        "estado_registro": "Nuevo",
        "hash_producto": hash_producto
    }

    res = upsert_producto(producto)
    print(res)
