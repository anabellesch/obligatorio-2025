# services/reserva_service.py
from db import get_conn
from utils import hour_int_from_time_str, validate_hours_between_8_23, week_bounds_for_date, is_docente, is_posgrado
from services.sanciones import SancionesService
from datetime import datetime, date, timedelta

class ReservaService:

    @staticmethod
    def crear(ci_solicitante, id_sala, fecha_str, hora_inicio_str, hora_fin_str, participantes_list):
        """
        - ci_solicitante: quien solicita (string CI)
        - id_sala: int
        - fecha_str: "YYYY-MM-DD"
        - hora_inicio_str: "HH:MM"
        - hora_fin_str: "HH:MM"
        - participantes_list: lista de CI de participantes (incluye solicitante si corresponde)
        """
        # parseo
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        h_start = hour_int_from_time_str(hora_inicio_str)
        h_end = hour_int_from_time_str(hora_fin_str)
        validate_hours_between_8_23(h_start, h_end)
        horas_a_reservar = h_end - h_start  # número de bloques

        # conexiones
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        try:
            # obtener sala
            cur.execute("SELECT id_sala, capacidad, tipo_sala FROM sala WHERE id_sala = %s", (id_sala,))
            sala = cur.fetchone()
            if not sala:
                raise ValueError("Sala no encontrada")

            # ver capacidad
            if len(participantes_list) > sala['capacidad']:
                raise ValueError("Cantidad de participantes excede la capacidad de la sala")

            # obtener tipo_sala para excepciones
            tipo_sala = sala['tipo_sala']  # 'libre', 'posgrado', 'docente'

            # regla: solicitante o participantes sancionados no pueden reservar
            for ci in participantes_list:
                cur.execute("""
                    SELECT 1 FROM sancion_participante
                    WHERE ci_participante = %s AND fecha_fin >= CURDATE() LIMIT 1
                """, (ci,))
                if cur.fetchone():
                    raise ValueError(f"El participante {ci} tiene sanción activa")

            # Validaciones por bloque: para cada turno (hora) debemos:
            #  - obtener id_turno
            #  - verificar disponibilidad de la sala para ese turno
            #  - verificar que ningún participante esté participando en otra reserva para ese mismo dia+turno
            #  - verificar límite de 2 horas diarias por participante (salvo excepciones)
            #  - verificar límite de 3 reservas activas en la semana por participante (salvo excepciones)
            # Precalculo: para cada participante, su rol
            roles_cache = {}
            for ci in participantes_list:
                roles_cache[ci] = {
                    "is_docente": is_docente(ci),
                    "is_posgrado": is_posgrado(ci)
                }

            # Empezamos transacción
            conn.start_transaction()

            for hour in range(h_start, h_end):
                # obtener id_turno
                cur.execute("SELECT id_turno FROM turno WHERE hora_inicio = MAKETIME(%s,0,0) LIMIT 1", (hour,))
                trow = cur.fetchone()
                if not trow:
                    raise ValueError(f"No existe turno para la hora {hour}:00")
                id_turno = trow['id_turno']

                # verificar disponibilidad sala
                cur.execute("""
                    SELECT 1 FROM reserva WHERE id_sala=%s AND fecha=%s AND id_turno=%s AND estado='activa' LIMIT 1
                """, (id_sala, fecha, id_turno))
                if cur.fetchone():
                    raise ValueError(f"Sala ocupada para el turno {hour}:00 - ya existe una reserva activa")

                # Para cada participante, verificar solapamiento (no puede participar en 2 reservas mismo dia+turno)
                for ci in participantes_list:
                    cur.execute("""
                        SELECT r.id_reserva
                        FROM reserva r
                        JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
                        WHERE rp.ci_participante = %s AND r.fecha = %s AND r.id_turno = %s AND r.estado = 'activa'
                        LIMIT 1
                    """, (ci, fecha, id_turno))
                    if cur.fetchone():
                        raise ValueError(f"El participante {ci} ya participa en otra reserva para el mismo turno ({hour}:00)")

                # Validaciones por participante: 2 horas diarias y 3 reservas semanales
                # Calculamos solo para los participantes que tienen la limitación (no docentes ni posgrado cuando la sala es exclusiva para ellos)
                for ci in participantes_list:
                    role = roles_cache[ci]
                    exempt_for_this_sala = False
                    if tipo_sala == "posgrado" and role["is_posgrado"]:
                        exempt_for_this_sala = True
                    if tipo_sala == "docente" and role["is_docente"]:
                        exempt_for_this_sala = True

                    if not exempt_for_this_sala:
                        # contar bloques ya reservados por el participante en esa fecha (solo salas no exclusivas)
                        cur.execute("""
                            SELECT COUNT(*) AS cnt
                            FROM reserva r
                            JOIN sala s ON r.id_sala = s.id_sala
                            WHERE r.fecha = %s AND r.solicitante_ci = %s AND r.estado = 'activa' AND s.tipo_sala = 'libre'
                        """, (fecha, ci))
                        cnt_today = cur.fetchone()['cnt'] or 0
                        # Note: estamos contando por solicitante_ci; si el participante no es solicitante chequeamos participación
                        # también chequeamos participación en reservas donde participa (no sólo las solicitadas)
                        cur.execute("""
                            SELECT COUNT(*) AS cntp
                            FROM reserva r
                            JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
                            JOIN sala s ON r.id_sala = s.id_sala
                            WHERE r.fecha = %s AND rp.ci_participante = %s AND r.estado = 'activa' AND s.tipo_sala = 'libre'
                        """, (fecha, ci))
                        cnt_today_particip = cur.fetchone()['cntp'] or 0

                        # Para la regla "no más de 2 horas diarias" interpretamos como: la suma de bloques en los que participa ese día
                        if (cnt_today_particip + 1) > 2:
                            raise ValueError(f"El participante {ci} excede las 2 horas diarias permitidas")

                        # contar reservas activas en la semana (distintas reservas) -> máx 3
                        start_w, end_w = week_bounds_for_date(fecha)
                        cur.execute("""
                            SELECT COUNT(DISTINCT r.id_reserva) AS cnt
                            FROM reserva r
                            JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
                            JOIN sala s ON r.id_sala = s.id_sala
                            WHERE rp.ci_participante = %s
                              AND r.fecha BETWEEN %s AND %s
                              AND r.estado = 'activa'
                        """, (ci, start_w, end_w))
                        cnt_week = cur.fetchone()['cnt'] or 0
                        if (cnt_week + 1) > 3:
                            raise ValueError(f"El participante {ci} excede las 3 reservas activas en la semana")

                # Si todas las validaciones del bloque pasaron, creamos la reserva para este turno
                # Insertar en reserva (solicitante_ci se guarda)
                cur.execute("""
                    INSERT INTO reserva (id_sala, id_edificio, fecha, id_turno, estado, solicitante_ci)
                    VALUES (%s, (SELECT id_edificio FROM sala WHERE id_sala = %s), %s, %s, 'activa', %s)
                """, (id_sala, id_sala, fecha, id_turno, ci_solicitante))
                id_res = cur.lastrowid

                # insertar participantes
                for ci in participantes_list:
                    cur.execute("""
                        INSERT INTO reserva_participante (ci_participante, id_reserva)
                        VALUES (%s, %s)
                    """, (ci, id_res))

            # todo ok -> commit
            conn.commit()
            return {"message": "Reservas creadas correctamente"}

        except Exception as e:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()


    @staticmethod
    def marcar_asistencia(id_reserva, ci_participante, asistencia: bool):
        """
        marca asistencia TRUE/FALSE para un participante en reserva_participante
        """
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE reserva_participante
                SET asistencia = %s
                WHERE id_reserva = %s AND ci_participante = %s
            """, (1 if asistencia else 0, id_reserva, ci_participante))
            if cur.rowcount == 0:
                raise ValueError("Registro de participante en reserva no encontrado")
            conn.commit()
            return {"message": "Asistencia registrada"}
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def cancelar_reserva(id_reserva):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
            if cur.rowcount == 0:
                raise ValueError("Reserva no encontrada")
            conn.commit()
            return {"message": "Reserva cancelada"}
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
