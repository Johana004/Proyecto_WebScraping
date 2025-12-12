Plataforma Avanzada para la Extracción de Datos en la Web y su Visualización
Este proyecto desarrolla una plataforma sólida para la recopilación de datos desde fuentes tanto fijas como dinámicas. Emplea PostgreSQL para la conservación de datos y el control de versiones, garantizando una detección precisa de modificaciones en los registros y archivos descargados mediante el uso de algoritmos hash (SHA-256). La automatización se coordina a través de apscheduler.

1. Estructura Final del Proyecto
La estructura a continuación organiza el código fuente, la configuración, los datos y la documentación del proyecto, siguiendo las mejores prácticas para un entorno de Docker y un desarrollo profesional.

proyecto_scraping/
├── api/                  # Módulo para la API de exposición de datos (Dashboard y JSON)
│   ├── templates/        # (Opcional) Archivos HTML/Jinja para el dashboard
│   └── app.py            # Servidor Flask para endpoints (JSON y HTML)
├── database/             # Módulo de gestión de la base de datos PostgreSQL
│   ├── db.py             # Funciones de conexión, lógica de Upsert (actualizar/insertar) y CRUD
│   └── esquema_completo.sql# Script SQL con la definición de tablas (productos, archivos, eventos)
├── data/                 # Archivos de salida (JSONs generados a partir de la DB)
│   ├── results.json      # Datos principales de productos extraídos
│   ├── events.json       # Logs y eventos de ejecución del scraper/scheduler
│   └── files.json        # Registro de la gestión de archivos descargados
├── docs/                 # Documentación del proyecto y guías
│   └── GETTING_STARTED.md# Guía de inicio rápido
├── **downloads/** # (FOLDER REQUERIDO) Carpeta local para almacenar archivos (PDFs, imágenes)
├── scraper/              # Módulos específicos de scraping
│   ├── scraper_dynamic.py# Lógica de scraping con Selenium/Playwright (sitios dinámicos)
│   └── scraper_static.py # Lógica de scraping con BeautifulSoup/Requests (sitios estáticos)
├── backups/              # Carpeta para respaldos de la Base de Datos (.bak)
├── .env                  # Archivo de Variables de Ambiente (IGNORADO por Git)
├── requirements.txt      # Dependencias de Python necesarias (psycopg2, selenium, apscheduler, etc.)
├── scheduler.py          # Script principal de automatización usando APScheduler
├── main.py               # Pipeline de ejecución que orquesta los scrapers y la lógica de DB
└── README.md             # Documento de descripción y configuración



2. Configuración Local
2.1 Requisitos Previos
Python versión 3.9 o superior (se sugiere emplear la misma versión que se utilizó para el desarrollo, por ejemplo, Python 3.13).

PostgreSQL de la versión 14 o más reciente.

Un navegador como Google Chrome o Microsoft Edge (necesario para el scraping dinámico según Selenium).

Git

2.2 Pasos de Instalación y Configuración
Clonar el Repositorio:

Bash

git clone [URL_DE_TU_REPOSITORIO]
cd proyecto_scraping
Establecer Entorno Virtual e Instalar Dependencias:

Bash

python -m venv venv
source venv/bin/activate # Linux/macOS
.\venv\Scripts\activate # Windows

pip install -r requirements.txt
Configurar el Archivo .env: Genere un archivo .env en la raíz del proyecto y establezca las variables de conexión a la base de datos (Consultar la Sección 3).

Inicializar la Base de Datos: Verifique que el servicio de PostgreSQL esté en funcionamiento. Cree la base de datos (por ejemplo, proyecto_scraping) y ejecute el script de esquema para crear las tablas necesarias:

Bash

psql -U DB_USER -d DB_NAME -f database/esquema_completo.sql


3. Variables del Entorno (.env)
Cree un archivo denominado .env en la carpeta principal del proyecto para guardar las credenciales de la Base de Datos y otros datos sensibles. Este archivo está programado para que Git lo ignore.

Ini, TOML

# Configuración de Conexión a PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=proyecto_scraping
DB_USER=postgres
DB_PASSWORD=su_contraseña_segura

# Configuración Opcional para Scraping Dinámico
# Use 'True' para operar sin una ventana de navegador (modo sin cabeza)
SELENIUM_HEADLESS=True

4. Descripción del Diseño
4.1. Estructura Modular y Flujo de Ejecución
El proyecto está diseñado de manera modular para distinguir claramente las diferentes responsabilidades:

Scraping y Extracción (scraper/): Emplea bibliotecas especializadas para interactuar con diferentes tipos de páginas web (Selenium para interacciones avanzadas; Requests/BS4 para contenidos estáticos y descargas directas).

Persistencia y Versionamiento (database/): El módulo db.py actúa como el núcleo que aplica la lógica de detección de cambios y gestión de versiones antes de almacenar la información.

Automatización (scheduler.py): apscheduler funciona como el coordinador, llamando a main.py para llevar a cabo el flujo de extracción y procesamiento en intervalos específicos, asegurando que los datos se mantengan actualizados (por ejemplo, cada 30 minutos).

Exposición (api/): Flask se utiliza para crear los endpoints que ofrecen los datos procesados y limpios (en formato JSON) así como un panel para su visualización.

4.2. Estrategia de Monitoreo de Cambios y Hash (SHA-256)
El aspecto fundamental del diseño es la robustez y la habilidad para supervisar la información, no solo para insertarla:
Crear Carpetas Necesarias: Asegúrese de que existan las carpetas para la gestión de archivos y los backups:

Bash

mkdir downloads
mkdir backups

Elemento Vigilado Método de Identificación Logística de Control de Versiones
Productos (Datos) Verificación del hash_producto Si el hash presenta cambios, se ajusta el estado_registro a 'Modificado', se anota un evento y se eleva el valor de la columna versión.
Archivos (Descargas) Verificación del hash_sha256 Si se recibe un archivo con un hash que no coincide con el registrado (en la misma URL), el archivo en ./downloads/ es sustituido. La entrada en archivos se actualiza con el nuevo hash.
Eventos/Registros Gestión organizada Cualquier acción (inserción, modificación, error) se documenta en la tabla de eventos, lo que posibilita un seguimiento completo del ciclo de vida de los datos.

4.3. Flujo Típico de Automatización
Comienzo del Scheduler (ejecutar python scheduler.py).

Tareas Programadas:

Realizar Scraping Dinámico.

Realizar Scraping Estático (incluida la descarga a ./downloads/).

Tratamiento de Datos: Los datos sin procesar se envían a db.py.

Lógica de la Base de Datos: Se generan los hashes y se lleva a cabo el upsert (identificación de cambios).

Generación de JSON: Se obtiene la información más reciente de la Base de Datos para reconstruir los archivos data/*.json, que estarán listos para la API.

Comandos 
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install selenium
pip install webdriver-manager
pip install undetected-chromedriver
pip install beautifulsoup4
pip install requests
pip install flask
pip install python-dotenv
pip install psycopg2
pip install psycopg2-binary
pip install apscheduler
pip install playwright
pip install --upgrade playwright
playwright install chromium


python test_dynamic.py
python test_static.py
python test_upsert.py
python generate_json.py
python json_api_server.py
python scheduler.py
  
