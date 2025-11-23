import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

def execute_query(query, params=None):
    """
    Ejecuta una consulta SQL y retorna los resultados
    
    Args:
        query: La consulta SQL a ejecutar
        params: Tupla de parámetros para la consulta (opcional)
    
    Returns:
        Lista de diccionarios con los resultados para SELECT
        Diccionario con affected_rows y last_id para INSERT/UPDATE/DELETE
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Si es un SELECT, retornar resultados
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            return results
        else:
            # Si es INSERT, UPDATE, DELETE, hacer commit
            conn.commit()
            return {"affected_rows": cursor.rowcount, "last_id": cursor.lastrowid}
    
    except mysql.connector.Error as err:
        conn.rollback()
        raise err
    
    finally:
        cursor.close()
        conn.close()

def execute_many(query, params_list):
    """
    Ejecuta múltiples inserts/updates en una transacción
    
    Args:
        query: La consulta SQL a ejecutar
        params_list: Lista de tuplas con parámetros
    
    Returns:
        Número de filas afectadas
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.executemany(query, params_list)
        conn.commit()
        return cursor.rowcount
    
    except mysql.connector.Error as err:
        conn.rollback()
        raise err
    
    finally:
        cursor.close()
        conn.close()


def get_conn():
    return get_db_connection()


def execute_transaction(queries_with_params):
    """
    Ejecuta múltiples queries en la misma transacción.

    queries_with_params: lista de tuplas (query, params)
    Retorna: lista de resultados de execute() para cada query (solo como referencia)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    results = []
    try:
        for q, p in queries_with_params:
            if p:
                cursor.execute(q, p)
            else:
                cursor.execute(q)
            # Guardar info mínima
            results.append({"affected_rows": cursor.rowcount, "last_id": cursor.lastrowid})
        conn.commit()
        return results
    except mysql.connector.Error as err:
        conn.rollback()
        raise err
    finally:
        cursor.close()
        conn.close()