# services/sala_service.py
from db import get_conn

class SalasService:

    @staticmethod
    def listar():
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id_sala, nombre_sala, id_edificio, capacidad, tipo_sala FROM sala")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows

    @staticmethod
    def obtener(id_sala):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id_sala, nombre_sala, id_edificio, capacidad, tipo_sala FROM sala WHERE id_sala = %s", (id_sala,))
        s = cur.fetchone()
        cur.close()
        conn.close()
        if not s:
            raise ValueError("Sala no encontrada")
        return s

    @staticmethod
    def verificar_disponibilidad(id_sala, fecha, id_turno):
        """
        Devuelve True si no existe reserva en la sala para la fecha y turno indicado.
        """
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 1 FROM reserva
            WHERE id_sala = %s AND fecha = %s AND id_turno = %s AND estado = 'activa'
            LIMIT 1
        """, (id_sala, fecha, id_turno))
        r = cur.fetchone()
        cur.close()
        conn.close()
        return r is None
