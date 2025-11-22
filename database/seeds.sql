USE gestion_salas;

-- Facultades y programas
INSERT INTO facultad (nombre) VALUES ('Ingeniería'), ('Derecho'), ('Ciencias Empresariales');

INSERT INTO programa_academico (nombre_programa, id_facultad, tipo)
VALUES
('Ingeniería Informática', 1, 'grado'),
('Ingeniería Ambiental', 1, 'grado'),
('Maestría en Derecho', 2, 'posgrado'),
('MBA', 3, 'posgrado');

-- Edificios
INSERT INTO edificio (nombre_edificio, direccion, departamento)
VALUES ('Central', 'Av. 8 de Octubre 1234', 'Montevideo'),
       ('San Ignacio', 'Av.8 de Octubre 4321', 'Montevideo');

-- Salas
INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala)
VALUES ('Sala A', 1, 6, 'libre'),
       ('Sala B', 1, 10, 'libre'),
       ('Sala Posgrado 1', 2, 8, 'posgrado'),
       ('Sala Docente 1', 2, 12, 'docente');

-- Turnos horarios (8 -> 22h)
INSERT INTO turno (hora_inicio, hora_fin)
VALUES ('08:00:00','09:00:00'), ('09:00:00','10:00:00'), ('10:00:00','11:00:00'),
       ('11:00:00','12:00:00'), ('12:00:00','13:00:00'), ('13:00:00','14:00:00'),
       ('14:00:00','15:00:00'), ('15:00:00','16:00:00'), ('16:00:00','17:00:00'),
       ('17:00:00','18:00:00'), ('18:00:00','19:00:00'), ('19:00:00','20:00:00'),
       ('20:00:00','21:00:00'), ('21:00:00','22:00:00');

-- Participantes de prueba
INSERT INTO participante (ci, nombre, apellido, email)
VALUES ('1000001','Ana','Gomez','ana.gomez@example.com'),
       ('1000002','Juan','Perez','juan.perez@example.com'),
       ('1000003','María','Lopez','maria.lopez@example.com');

-- Programas y roles
INSERT INTO participante_programa_academico (ci_participante, id_programa, rol)
VALUES ('1000001', 1, 'alumno'),
       ('1000002', 3, 'docente'),
       ('1000003', 4, 'alumno');


