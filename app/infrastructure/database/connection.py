# app/infrastructure/database/connection.py
import sqlite3
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

class Database:
    """Clase para gestionar la conexión a la base de datos SQLite"""
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implementación de patrón Singleton para la conexión a base de datos"""
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path: str = None):
        """Inicializa la conexión a la base de datos"""
        if self._initialized:
            return
            
        # Si no se proporciona una ruta, usamos una por defecto
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            db_path = os.path.join(base_dir, 'data', 'power_automate.db')
            
            # Asegurarse de que el directorio existe
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.connection = None
        self._initialized = True
    
    def connect(self):
        """Establece la conexión a la base de datos"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Ejecuta una consulta SQL"""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return cursor
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
        """Ejecuta una consulta y devuelve un solo resultado"""
        cursor = self.execute(query, params)
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Ejecuta una consulta y devuelve todos los resultados"""
        cursor = self.execute(query, params)
        results = cursor.fetchall()
        return [dict(row) for row in results]

# app/infrastructure/database/schema.py
from app.infrastructure.database.connection import Database

class DatabaseSchema:
    """Clase para gestionar el esquema de la base de datos"""
    
    @staticmethod
    def create_tables():
        """Crea las tablas necesarias en la base de datos"""
        db = Database()
        
        # Tabla de proyectos
        db.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        
        # Tabla de flujos
        db.execute('''
            CREATE TABLE IF NOT EXISTS flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                recurrence TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                owner TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
            )
        ''')
        
        db.disconnect()
        
    @staticmethod
    def drop_tables():
        """Elimina las tablas de la base de datos"""
        db = Database()
        db.execute('DROP TABLE IF EXISTS flows')
        db.execute('DROP TABLE IF EXISTS projects')
        db.disconnect()