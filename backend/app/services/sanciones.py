from db import get_conn
from datetime import datetime, timedelta

class SancionesService:

    @staticmethod
    def crear(ci_participante, dias=60, motivo="No asistencia a reserva"):
        """
        Inserta sancion_participante (ci_participante, fecha_inicio, fecha_fin)
        por defecto 60 dias (2 meses ~ 60 días)
        """
        fecha_inicio = datetime.utcnow().date()
        fecha_fin = fecha_inicio + timedelta(days=dias)
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin, motivo)
                VALUES (%s,%s,%s,%s)
            """, (ci_participante, fecha_inicio, fecha_fin, motivo))
            conn.commit()
            return {"message": "Sanción creada"}
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def tiene_sancion_activa(ci):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 1 FROM sancion_participante
            WHERE ci_participante = %s AND fecha_fin >= CURDATE()
            LIMIT 1
        """, (ci,))
        r = cur.fetchone()
        cur.close()
        conn.close()
        return bool(r)
