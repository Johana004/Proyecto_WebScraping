# database/db.py
import os
import subprocess
import json
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.scraper_logger import log_event  # LOG JSON → scraper.log

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "proyecto_scraping")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ---------------------------------------------------------
# Logging en PostgreSQL
# ---------------------------------------------------------
def log(tipo, mensaje, nivel="INFO", referencia_tipo=None, referencia_id=None, metadata=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO logs (nivel, tipo, mensaje, referencia_tipo, referencia_id, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nivel, tipo, mensaje, referencia_tipo, referencia_id, json.dumps(metadata)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        log_event("ERROR", "Falló el insert en tabla logs", {"error": str(e)})

# ---------------------------------------------------------
# Upsert producto
# ---------------------------------------------------------
def upsert_producto(producto: dict):
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT id, hash_producto, version FROM productos WHERE url_origen = %s",
            (producto["url_origen"],)
        )
        row = cur.fetchone()

        # ---------------------------------
        # INSERTAR NUEVO PRODUCTO
        # ---------------------------------
        if row is None:
            cur.execute("""
                INSERT INTO productos (titulo, precio, url_origen, oferta, cantidad, estado_registro,
                    hash_producto, version, last_seen)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now())
                RETURNING id;
            """, (
                producto["titulo"],
                producto["precio"],
                producto["url_origen"],
                producto.get("oferta", False),
                producto.get("cantidad"),
                "Nuevo",
                producto["hash_producto"],
                1
            ))
            new_id = cur.fetchone()["id"]

            conn.commit()
            cur.close()
            conn.close()

            # LOG a BD
            log("producto", f"Producto insertado: {producto['url_origen']}",
                referencia_tipo="producto", referencia_id=new_id)

            # LOG JSON
            log_event("INSERT", "Producto insertado", {
                "id": new_id,
                "url": producto["url_origen"],
                "precio": producto["precio"]
            })

            return {"action": "inserted", "id": new_id}

        # ---------------------------------
        # YA EXISTE – COMPARAR HASH
        # ---------------------------------
        existing_hash = row["hash_producto"]
        pid = row["id"]
        version = row["version"]

        if existing_hash != producto["hash_producto"]:
            # UPDATE → incrementar version
            new_version = version + 1

            cur.execute("""
                UPDATE productos
                SET titulo=%s, precio=%s, oferta=%s, cantidad=%s, estado_registro=%s,
                    hash_producto=%s, version=%s, last_seen=now(), fecha_extraccion=now()
                WHERE id=%s
            """, (
                producto["titulo"],
                producto["precio"],
                producto.get("oferta", False),
                producto.get("cantidad"),
                "Modificado",
                producto["hash_producto"],
                new_version,
                pid
            ))

            conn.commit()
            cur.close()
            conn.close()

            # LOG BD
            log("producto", f"Producto actualizado: {producto['url_origen']} (v{new_version})",
                referencia_tipo="producto", referencia_id=pid)

            # LOG JSON
            log_event("UPDATE", "Producto actualizado", {
                "id": pid,
                "version_nueva": new_version,
                "url": producto["url_origen"]
            })

            return {"action": "updated", "id": pid, "version": new_version}

        # ---------------------------------
        # SIN CAMBIOS
        # ---------------------------------
        cur.execute("UPDATE productos SET last_seen = now() WHERE id = %s", (pid,))
        conn.commit()
        cur.close()
        conn.close()

        # LOG JSON
        log_event("NO_CHANGE", "Producto sin cambios", {
            "id": pid,
            "url": producto["url_origen"]
        })

        return {"action": "unchanged", "id": pid}

    except Exception as e:
        log_event("ERROR", "Error en upsert_producto", {"error": str(e)})
        raise e

# ---------------------------------------------------------
# Insertar archivo descargado
# ---------------------------------------------------------
def insertar_archivo(archivo: dict):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO archivos (producto_id, nombre_archivo, ruta_local, url_origen, hash_sha256, estado_archivo)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            archivo.get("producto_id"),
            archivo["nombre_archivo"],
            archivo["ruta_local"],
            archivo["url_origen"],
            archivo["hash_sha256"],
            archivo.get("estado_archivo", "Nuevo")
        ))
        aid = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        log("archivo", f"Archivo insertado: {archivo['nombre_archivo']}",
            referencia_tipo="archivo", referencia_id=aid)

        log_event("INSERT", "Archivo insertado", {
            "id": aid,
            "nombre": archivo["nombre_archivo"]
        })

        return aid

    except Exception as e:
        log_event("ERROR", "Error al insertar archivo", {"error": str(e)})
        raise e

# ---------------------------------------------------------
# Eventos calendario
# ---------------------------------------------------------
def crear_evento(titulo, descripcion, fecha_inicio, fecha_fin=None, tipo="info", metadata=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO eventos (titulo, descripcion, fecha_inicio, fecha_fin, tipo, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (titulo, descripcion, fecha_inicio, fecha_fin, tipo,
              json.dumps(metadata) if metadata else None))

        eid = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        log("evento", f"Evento creado: {titulo}", referencia_tipo="evento", referencia_id=eid)

        log_event("EVENT", "Evento creado", {
            "id": eid,
            "titulo": titulo
        })

        return eid

    except Exception as e:
        log_event("ERROR", "Error al crear evento", {"error": str(e)})
        raise e

# ---------------------------------------------------------
# Backups
# ---------------------------------------------------------
def crear_backup_sql(output_dir="backups"):
    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(output_dir, f"{DB_NAME}_{ts}.sql")

    try:
        cmd = [
            "pg_dump",
            "-h", DB_HOST,
            "-p", str(DB_PORT),
            "-U", DB_USER,
            "-F", "c",
            "-f", out,
            DB_NAME
        ]

        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASS

        subprocess.check_call(cmd, env=env)
        log("backup", f"Backup creado {out}")
        log_event("BACKUP", "Backup SQL creado", {"archivo": out})

        return out

    except Exception as e:
        log_event("ERROR", "Error en backup SQL", {"error": str(e)})
        raise e

# ---------------------------------------------------------
# Obtener producto por URL
# ---------------------------------------------------------
def get_producto_por_url(url_origen):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM productos WHERE url_origen = %s", (url_origen,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row
