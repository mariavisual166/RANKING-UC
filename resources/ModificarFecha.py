import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.scholar import main
import time
import datetime
from datetime import datetime

def CambiarFechaTope(faces,facyt,face,odontologia,fcjp,ingieneria,derecho):
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

    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(facyt,"Facyt")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(faces,"Faces")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(face,"Face")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(odontologia,"Odontologia")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(fcjp,"Fcjp")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(ingieneria,"Ingieneria")
    cur.execute(Fecha)
    Fecha = "  UPDATE FechaTope SET Fecha='{}'WHERE Facultad='{}';".format(derecho,"Fcs")
    cur.execute(Fecha)

    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Facyt")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Faces")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Face")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Odontologia")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Fcjp")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Ingieneria")
    cur.execute(Enviado)
    Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("False","Fcs")
    cur.execute(Enviado)
    conn.commit()
    cur.close()
    conn.close()