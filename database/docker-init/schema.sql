-- schema.sql
CREATE DATABASE IF NOT EXISTS gestion_salas;
USE gestion_salas;

-- Facultades
CREATE TABLE facultad (
  id_facultad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE
);

-- Programas académicos
CREATE TABLE programa_academico (
  id_programa INT AUTO_INCREMENT PRIMARY KEY,
  nombre_programa VARCHAR(150) NOT NULL,
  id_facultad INT NOT NULL,
  tipo ENUM('grado','posgrado') NOT NULL,
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

-- Participantes (CI como identificador principal)
CREATE TABLE participante (
  ci VARCHAR(20) PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(150) NOT NULL UNIQUE
);

-- Relación participante - programa (rol: alumno/docente)
CREATE TABLE participante_programa_academico (
  id_alumno_programa INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  id_programa INT NOT NULL,
  rol ENUM('alumno','docente') NOT NULL,
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa),
  UNIQUE (ci_participante, id_programa)
);

-- Edificios
CREATE TABLE edificio (
  id_edificio INT AUTO_INCREMENT PRIMARY KEY,
  nombre_edificio VARCHAR(150) NOT NULL UNIQUE,
  direccion VARCHAR(250),
  departamento VARCHAR(100)
);

-- Salas
CREATE TABLE sala (
  id_sala INT AUTO_INCREMENT PRIMARY KEY,
  nombre_sala VARCHAR(100) NOT NULL,
  id_edificio INT NOT NULL,
  capacidad INT NOT NULL CHECK (capacidad > 0),
  tipo_sala ENUM('libre','posgrado','docente') NOT NULL,
  FOREIGN KEY (id_edificio) REFERENCES edificio(id_edificio),
  UNIQUE (nombre_sala, id_edificio)
);

-- Turnos (bloques de 1 hora)
CREATE TABLE turno (
  id_turno INT AUTO_INCREMENT PRIMARY KEY,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  UNIQUE (hora_inicio, hora_fin)
);

-- Reserva (1 fila = 1 bloque de 1 hora en una sala)
CREATE TABLE reserva (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  id_sala INT NOT NULL,
  fecha DATE NOT NULL,
  id_turno INT NOT NULL,
  estado ENUM('activa','cancelada','sin asistencia','finalizada') NOT NULL DEFAULT 'activa',
  fecha_solicitud DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno),
  -- no permitir doble reserva del mismo bloque en la misma sala
  UNIQUE KEY uq_reserva_sala_fecha_turno (id_sala, fecha, id_turno),
  INDEX ix_reserva_fecha (fecha),
  INDEX ix_reserva_estado (estado)
);

-- Reserva-Participante (participantes asociados a una reserva)
CREATE TABLE reserva_participante (
  ci_participante VARCHAR(20) NOT NULL,
  id_reserva INT NOT NULL,
  fecha_solicitud_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  asistencia TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (ci_participante, id_reserva),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

-- Sanciones
CREATE TABLE sancion_participante (
  id_sancion INT AUTO_INCREMENT PRIMARY KEY,
  ci_participante VARCHAR(20) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  motivo VARCHAR(255),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

-- Login separado (referencia a participante por ci)
CREATE TABLE login (
  correo VARCHAR(150) PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL,
  ci_participante VARCHAR(20),
  rol_sistema ENUM('admin','usuario') DEFAULT 'usuario',
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);
