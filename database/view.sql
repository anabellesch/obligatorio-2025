USE gestion_salas;

-- Salas más reservadas
CREATE OR REPLACE VIEW v_salas_mas_reservadas AS
SELECT s.id_sala, s.nombre_sala, e.nombre_edificio, COUNT(*) AS total_reservas
FROM reserva r
JOIN sala s ON r.id_sala = s.id_sala
JOIN edificio e ON s.id_edificio = e.id_edificio
GROUP BY s.id_sala
ORDER BY total_reservas DESC;

-- Turnos más demandados
CREATE OR REPLACE VIEW v_turnos_mas_demandados AS
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(*) AS total
FROM reserva r JOIN turno t ON r.id_turno = t.id_turno
GROUP BY t.id_turno
ORDER BY total DESC;

-- Promedio de participantes por sala (promedio por reserva)
CREATE OR REPLACE VIEW v_promedio_participantes_por_sala AS
SELECT s.id_sala, s.nombre_sala, AVG(cnt) AS promedio_participantes
FROM (
  SELECT id_reserva, COUNT(*) AS cnt FROM reserva_participante GROUP BY id_reserva
) rp
JOIN reserva r ON rp.id_reserva = r.id_reserva
JOIN sala s ON r.id_sala = s.id_sala
GROUP BY s.id_sala;
