
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import psycopg2
# create message object instance
from datetime import datetime,timedelta
from flask_restful import abort
import simplejson as json
import pymysql
import time
import datetime
def obtenerCorreo(user):

    # Abre conexion con la base de datos
    db = pymysql.connect("localhost","root","root","prueba")
    ##################################################
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # ejecuta el SQL query usando el metodo execute().
    cursor.execute("SELECT email FROM USER WHERE username='{}'".format(user))
    rows=cursor.fetchone()
    # desconecta del servidor
    db.close()
    return(rows[0])
def ValidarFecha(FechaTope):
    logico=False

    FechaActual = time.strftime('%Y-%m-%d %H:%M:%S')
 
    if str(FechaActual) > str(FechaTope):
       logico=True
    
        
    return (logico)
def enviarCorreo(destino,mensaje):
    msg = MIMEMultipart()
    message = mensaje
    # setup the parameters of the message
    password = "--maria--1994"
    msg['From'] = "mariangelagm8@gmail.com"
    msg['To'] = destino
    msg['Subject'] = "Subscription"
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print ("successfully sent email to %s:" % (msg['To']))
def enviarCorreoUsuario():
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    logico=""
  

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Facyt';"
    cur.execute(sqlquery7)
    Facyt=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Facyt';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()
    

    if(ValidarFecha(Facyt[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Facyt y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Facyt_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Facyt")
        cur.execute(Enviado)
        #data1={"username":user,"action": "Enviar correo  a Facyt", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Faces';"
    cur.execute(sqlquery7)
    Faces=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Faces';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()

    if(ValidarFecha(Faces[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Faces y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Faces_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Faces")
        cur.execute(Enviado)
        #data1={"username":user,"action": "Enviar correo  a Faces", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Face';"
    cur.execute(sqlquery7)
    Face=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE  Facultad='Face';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()

    if(ValidarFecha(Face[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Face y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Face_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Face")
        cur.execute(Enviado)
         #data1={"username":user,"action": "Enviar correo  a Face", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Odontologia';"
    cur.execute(sqlquery7)
    Odontologia=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Odontologia';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()
    if(ValidarFecha(Odontologia[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Odontologia y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Odontologia_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Odontologia")
        cur.execute(Enviado)
        #data1={"username":user,"action": "Enviar correo  a Odontologia", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))


    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Fcjp';"
    cur.execute(sqlquery7)
    Fcjp=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Fcjp';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()

    if(ValidarFecha(Fcjp[0])and Logico[0]=="False" ):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Fcjp y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Fcjp_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Fcjp")
        cur.execute(Enviado)
        #data1={"username":user,"action": "Enviar correo  a Fcjp", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Ingieneria';"
    cur.execute(sqlquery7)
    Ingieneria=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Ingieneria';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()

    if(ValidarFecha(Ingieneria[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Ingeneria y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Ingeneria_docente")
        enviarCorreo(correo,mensaje)
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Ingeneria")
        cur.execute(Enviado)
        #data1={"username":user,"action": "Enviar correo  a Ingieneria", "module": "Docentes"}
        #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Fcs';"
    cur.execute(sqlquery7)
    Derecho=cur.fetchone()
    sqlquery7 = "SELECT logico FROM CorreoEnviado WHERE Facultad='Fcs';"
    cur.execute(sqlquery7)
    Logico=cur.fetchone()

    if(ValidarFecha(Derecho[0]) and Logico[0]=="False"):
        mensaje="Primero que nada un cordial saludo de parte de Vicerrectodaro Academico de la Universidad de Carabobo . se le recuerda que la fecha para subir archivo de los docentes de Fcs y sus plublicaciones ya Expiro. Por  lo cual se le recuerda que debe subir el archivo correspondiente al Ranking UC.  "
        correo=obtenerCorreo("Fcs_docente")
        enviarCorreo(correo,mensaje)
        #data1={"username":user,"action": "Enviar correo  a Fcs", "module": "Docentes"}
                #r=requests.post("http://localhost:8084/api/v1/historyaction", data= json.dumps(data1))
        Enviado = "  UPDATE CorreoEnviado SET Logico='{}'WHERE Facultad='{}';".format("True","Fcs")
        cur.execute(Enviado)
    
    
    conn.commit()
    cur.close()
    conn.close()
def main_():
    print("corriendo ...")
    while (True):
        enviarCorreoUsuario()
        time.sleep(0.50)

main_()
