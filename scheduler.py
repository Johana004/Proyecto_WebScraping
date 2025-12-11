# scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.scraper_dynamic import ejecutar_scraper_dinamico
from scraper.scraper_static import scrape_estatico
from generate_json import generar_todos
from database.db import crear_evento
from datetime import datetime

scheduler = BlockingScheduler()

# -----------------------------
# TAREA 1: Scraping dinámico
# -----------------------------
@scheduler.scheduled_job("interval", minutes=30)
def tarea_scraping_dinamico():
    print("▶ Ejecutando scraping dinámico...")
    try:
        ejecutar_scraper_dinamico(query="laptops", max_pages=1, headless=True)
        crear_evento(
            titulo="Scraping dinámico ejecutado",
            descripcion="Scraping de Amazon finalizado correctamente",
            fecha_inicio=datetime.now(),
            tipo="success"
        )
    except Exception as e:
        print("❌ Error scraping dinámico:", e)
        crear_evento(
            titulo="Error en scraping dinámico",
            descripcion=str(e),
            fecha_inicio=datetime.now(),
            tipo="error"
        )

# -----------------------------
# TAREA 2: Scraping estático
# -----------------------------
@scheduler.scheduled_job("interval", minutes=30)
def tarea_scraping_estatico():
    print("▶ Ejecutando scraping estático...")
    try:
        scrape_estatico("http://localhost:5000/static-files")
        crear_evento(
            titulo="Scraping estático ejecutado",
            descripcion="Archivos estáticos actualizados",
            fecha_inicio=datetime.now(),
            tipo="info"
        )
    except Exception as e:
        print("❌ Error scraping estático:", e)
        crear_evento(
            titulo="Error en scraping estático",
            descripcion=str(e),
            fecha_inicio=datetime.now(),
            tipo="error"
        )

# -----------------------------
# TAREA 3: Regenerar JSONs
# -----------------------------
@scheduler.scheduled_job("interval", minutes=30)
def tarea_json():
    print("▶ Regenerando JSONs...")
    try:
        generar_todos()
        crear_evento(
            titulo="JSON actualizado",
            descripcion="Se regeneraron los JSON para el dashboard",
            fecha_inicio=datetime.now(),
            tipo="info"
        )
    except Exception as e:
        print("❌ Error en JSON:", e)
        crear_evento(
            titulo="Error al generar JSON",
            descripcion=str(e),
            fecha_inicio=datetime.now(),
            tipo="error"
        )

print("⏳ Scheduler iniciado. Ejecutando tareas cada 30 minutos…")
scheduler.start()
