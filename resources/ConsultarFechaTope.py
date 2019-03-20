import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.scholar import main
import time
import datetime
from datetime import datetime


def ConsultarFechaTopeE(Facultad):
#conexion a la base de datos
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
     #
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()

    Fecha = "  SELECT fecha FROM FechaTope WHERE Facultad='{}' ;".format(Facultad)
    cur.execute(Fecha)
    row=cur.fetchone()
    print(row[0]);
    conn.commit()
    cur.close()
    conn.close()
    
    FechaTopeU=row[0].strftime('%Y-%m-%d')
    FechaTopeU=FechaTopeU.replace('-', '/')
    return(FechaTopeU) ;