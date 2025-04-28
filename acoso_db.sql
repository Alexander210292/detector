-- Crear la base de datos (opcional si ya existe)
CREATE DATABASE acoso_db;

-- Usar la base de datos
\c acoso_db;

-- Crear la tabla Usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contraseña VARCHAR(100) NOT NULL
);

-- Crear la tabla Captura
CREATE TABLE captura (
    id SERIAL PRIMARY KEY,
    ruta_imagen VARCHAR(200) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
