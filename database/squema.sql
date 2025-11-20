-- esquema.sql COMPLETO

-- ============================================
-- 1. TABLA DE PRODUCTOS (Datos Estructurados)
-- ============================================
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    url_origen TEXT NOT NULL UNIQUE,
    fecha_extraccion TIMESTAMP WITH TIME ZONE DEFAULT now(),
    oferta BOOLEAN DEFAULT FALSE,
    cantidad INTEGER NULL,
    estado_registro VARCHAR(50) NOT NULL DEFAULT 'Nuevo',  -- Nuevo, Modificado, Eliminado
    hash_producto VARCHAR(64) NOT NULL,                    -- SHA256 del registro para detectar cambios
    version INTEGER NOT NULL DEFAULT 1                     -- Para control de versiones
);

CREATE INDEX IF NOT EXISTS idx_productos_url
ON productos(url_origen);


-- ============================================
-- 2. TABLA DE ARCHIVOS (Descarga y Detección)
-- ============================================
CREATE TABLE IF NOT EXISTS archivos (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255) NOT NULL,
    hash_sha256 VARCHAR(64) NOT NULL,
    url_origen TEXT NOT NULL,
    ruta_local TEXT NOT NULL,
    estado_archivo VARCHAR(50) NOT NULL DEFAULT 'Nuevo',   -- Nuevo, Modificado, Eliminado
    fecha_descarga TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_archivos_hash
ON archivos(hash_sha256);


-- ============================================
-- 3. TABLA DE LOGS (Histórico de Cambios)
-- ============================================
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,              -- inserción, modificación, eliminación, archivo cambio, etc
    descripcion TEXT NOT NULL,
    referencia_id INTEGER NULL,             -- ID al que afecta (producto o archivo)
    fecha_log TIMESTAMP WITH TIME ZONE DEFAULT now()
);


-- ============================================
-- 4. TABLA DE EVENTOS (Para FullCalendar.js)
-- ============================================
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    fecha_evento TIMESTAMP WITH TIME ZONE NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'info'   -- info, error, cambio, scraping, etc.
);


-- ============================================
-- 5. CONFIRMAR TRANSACCIÓN
-- ============================================
COMMIT;
