USE gestion_salas;
DELIMITER $$

-- BEFORE INSERT en reserva_participante: controla capacidad y límites por participante
CREATE TRIGGER trg_res_part_before_insert
BEFORE INSERT ON reserva_participante
FOR EACH ROW
BEGIN
  DECLARE sala_cap INT;
  DECLARE current_count INT;
  DECLARE p_rol VARCHAR(20);
  DECLARE p_tipo_programa VARCHAR(20);
  DECLARE room_type VARCHAR(20);
  DECLARE target_date DATE;
  DECLARE day_count INT;
  DECLARE week_count INT;

  -- obtener capacidad y tipo de sala para la reserva
  SELECT s.capacidad, s.tipo_sala INTO sala_cap, room_type
  FROM reserva r JOIN sala s ON r.id_sala = s.id_sala
  WHERE r.id_reserva = NEW.id_reserva
  LIMIT 1;

  -- contar participantes actuales en la reserva
  SELECT COUNT(*) INTO current_count FROM reserva_participante WHERE id_reserva = NEW.id_reserva;

  IF current_count + 1 > sala_cap THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Capacidad de la sala excedida';
  END IF;

  -- obtener rol y tipo de programa (si hay varios, se toma el primero)
  SELECT pp.rol, pa.tipo INTO p_rol, p_tipo_programa
  FROM participante_programa_academico pp
  JOIN programa_academico pa ON pp.id_programa = pa.id_programa
  WHERE pp.ci_participante = NEW.ci_participante
  LIMIT 1;

  -- aplicar límites solo si el participante es alumno de grado o rol='alumno' y la sala no es exclusiva para posgrado o docente
  IF (p_rol = 'alumno' AND p_tipo_programa = 'grado') THEN
    -- fecha de la reserva
    SELECT fecha INTO target_date FROM reserva WHERE id_reserva = NEW.id_reserva LIMIT 1;

    -- contar reservas en ese día (cada fila = 1 hora)
    SELECT COUNT(*) INTO day_count
    FROM reserva r JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
    WHERE rp.ci_participante = NEW.ci_participante
      AND r.fecha = target_date
      AND r.estado = 'activa';

    IF day_count + 1 > 2 THEN
       SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Excede el límite diario de 2 horas';
    END IF;

    -- contar reservas activas en la misma semana (semana ISO)
    SELECT COUNT(DISTINCT r.id_reserva) INTO week_count
    FROM reserva r JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
    WHERE rp.ci_participante = NEW.ci_participante
      AND WEEK(r.fecha, 1) = WEEK(target_date, 1)
      AND r.estado = 'activa';

    IF week_count + 1 > 3 THEN
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Excede el límite semanal de 3 reservas activas';
    END IF;
  END IF;

END$$

-- EVENT programado para marcar "sin asistencia" y generar sanciones
SET GLOBAL event_scheduler = ON;
CREATE EVENT IF NOT EXISTS ev_check_no_shows
ON SCHEDULE EVERY 1 HOUR
DO
BEGIN
  -- Actualiza reservas del pasado o el dia que no tuvieron asistencia
  UPDATE reserva r
  SET r.estado = 'sin asistencia'
  WHERE r.estado = 'activa'
    AND r.fecha < CURDATE()
    AND NOT EXISTS (
      SELECT 1 FROM reserva_participante rp WHERE rp.id_reserva = r.id_reserva AND rp.asistencia = 1
    );

  -- Insertar sanciones de 2 meses para participantes que no asistieron en reservas sin asistencia
  INSERT IGNORE INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin, motivo)
  SELECT rp.ci_participante, CURDATE(), DATE_ADD(CURDATE(), INTERVAL 2 MONTH), 'No asistió a reserva'
  FROM reserva r
  JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
  WHERE r.estado = 'sin asistencia';
END$$

DELIMITER ;
