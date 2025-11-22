# services/reporte_service.py
from db import get_conn
from services.sanciones import SancionesService
from datetime import datetime

class ReportesService:

    @staticmethod
    def crear(ci_participante, descripcion, tipo=None):
        conn = get_conn()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO reporte (ci_participante, descripcion, tipo, fecha)
                VALUES (%s, %s, %s, %s)
            """, (ci_participante, descripcion, tipo, datetime.utcnow()))
            conn.commit()
            # sancionar automáticamente si aplica
            if tipo in ("daño", "ausencia"):
                SancionesService.crear(ci_participante, dias=60, motivo=f"Sanción por reporte tipo {tipo}")
            return {"message": "Reporte creado"}
        except Exception:
            conn.rollback()
            raise
        finally:
            cur.close()
            conn.close()
