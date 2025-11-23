Sistema de Gestión de Reserva de Salas de Estudio — Introducción

Este proyecto implementa un sistema completo para la gestión de reservas de salas de estudio dentro del ámbito universitario. Permite administrar salas, participantes, reservas, asistencias, sanciones y generar reportes analíticos, cumpliendo con los requisitos del Trabajo Obligatorio del curso Base de Datos 1 (UCU — 2025).

La aplicación está construida con:

Backend en Python (sin ORM, siguiendo las restricciones del obligatorio).

Base de datos MySQL.

Frontend moderno (JavaScript).

Docker para facilitar el despliegue en cualquier entorno.

A continuación se detallan los pasos necesarios para ejecutar el proyecto localmente.

Cómo iniciar el proyecto

Antes de empezar, asegurate de tener instalados:

Docker

Docker Compose

Node.js + npm

1. Construir los contenedores con: 
docker compose build --no-cache

2. Levantar los servicios con: 
docker compose up


Esto iniciará:

El backend en Python

La base de datos MySQL

Otros servicios definidos en docker-compose.yml

3. Iniciar el frontend

Una vez iniciado Docker, accedé al directorio del frontend:

cd frontend


Instalá las dependencias:

npm install


Ejecutá el servidor de desarrollo:

npm run dev


El sistema quedará disponible en tu navegador en el puerto indicado por el frontend (generalmente http://localhost:5173 o similar).