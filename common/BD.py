from db_credentials import postgresql_db_config
#import pymysql
import psycopg2
from flask import make_response
from flask_restful import reqparse

class BD:
    
    conn = None
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    
    def connect(self):
        """Consulta las propiedades de conexión del archivo user.properties en la sección [DB]
        y crea la conexión a la base de datos. Esto se realiza una sola vez por cada instancia de la clase."""
        self.conn = psycopg2.connect(**postgresql_db_config)
        
    def queryAll(self, sql: str, params: list=[], columns: list=None):
        """
        Ejecuta una consulta a la base de datos y devuelve todos los registros.
        
        :param sql: Comando SELECT a ejecutar.
        :param params: Lista de parámetros para asociar al comando SELECT.
        :param columns: Lista opcional de nombres de columnas para los registros consultados.\n
            Si no se especifica este parámetro los registros se devuelven con los nombres de columnas retornados por
            la consulta ejecutada.
        :return: Retorna una lista de diccionarios con los datos de cada registro retornado por la consulta ejecutada.\n
            Ej. [{"id": 1, "first_name": "Jose", ...}, ...]
        """
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
	
        if columns is None:
            columns = [column[0].lower() for column in cursor.description]
        cursor.close()
        return [dict(zip(columns, row)) for row in rows]
        
    def queryOne(self, sql: str, params: list=[], columns: list=None):
        """
        Ejecuta una consulta a la base de datos y devuelve el primer registro.

        :param sql: Comando SELECT a ejecutar.
        :param params: Lista de parámetros para asociar al comando SELECT.
        :param columns: Lista opcional de nombres de columnas para los registros consultados.\n
            Si no se especifica este parámetro los registros se devuelven con los nombres de columnas retornados por
            la consulta ejecutada.
        :return: Retorna un diccionario con los datos del primer registro retornado por la consulta ejecutada.\n
            Ej. {"id": 1, "first_name": "Jose", ...}
        """
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        row = cursor.fetchone()
        if row is None:
            return None
        if columns is None:
            columns = [column[0].lower() for column in cursor.description]
        cursor.close()
        return dict(zip(columns, row))