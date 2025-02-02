import sqlite3
from functools import wraps
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class AutomationDBHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # This allows accessing columns by name
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def db_operation(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = None
            try:
                conn = self._get_connection()
                result = func(self, conn, *args, **kwargs)
                return result
            except sqlite3.Error as e:
                logger.error(f"Database operation error in {func.__name__}: {e}")
                raise
            finally:
                if conn:
                    conn.close()
        return wrapper

    @db_operation
    def get_environments(self, conn) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, code FROM environments ORDER BY name")
        return [dict(row) for row in cursor.fetchall()]

    @db_operation
    def get_components(self, conn, environment_id: int) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, code 
            FROM components 
            WHERE environment_id = ? 
            ORDER BY name
        """, (environment_id,))
        return [dict(row) for row in cursor.fetchall()]

    @db_operation
    def get_packets(self, conn, component_id: int) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, code 
            FROM packets 
            WHERE component_id = ? 
            ORDER BY name
        """, (component_id,))
        return [dict(row) for row in cursor.fetchall()]

    @db_operation
    def get_parameters(self, conn, packet_id: int) -> List[Dict[str, Any]]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, code, data_type 
            FROM parameters 
            WHERE packet_id = ? 
            ORDER BY name
        """, (packet_id,))
        return [dict(row) for row in cursor.fetchall()]