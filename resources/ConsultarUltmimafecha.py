import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.scholar import main
import time
import datetime
from datetime import datetime


def UltimaFecha(facultad):
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
     #
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    resul=""
    ObtId = "SELECT FechaActualizacion FROM Docente WHERE FechaActualizacion=(SELECT MAX(FechaActualizacion) from Docente) and Facultad='{}';".format(facultad)
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        resul= row[0]
    else:

        resul="No se ha relizado ninguna actualización "

    return(resul)
def ActualizacionApi():
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
     #
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    resul=""
    ObtId = "SELECT Fecha FROM FechaApi WHERE Fecha=(SELECT MAX(Fecha) from FechaApi) "
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        resul= row[0]
    else:

        resul="No se ha relizado ninguna actualización "

    return(resul)
