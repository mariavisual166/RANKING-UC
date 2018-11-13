
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import psycopg2
# create message object instance
from datetime import datetime,timedelta

def ValidarFecha(FechaTope):
    logico=False

    FechaActual = datetime.now().date()
 
    if str(FechaActual) > str(FechaTope):
       logico=True
    
        
    return (logico)

def enviarCorreo(destino,mensaje):
    msg = MIMEMultipart()
    message = "Thank you"
    # setup the parameters of the message
    password = "--maria--1994"
    msg['From'] = "mariangelagm8@gmail.com"
    msg['To'] = "gordita902@hotmail.com"
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


def enviarCorreoUsuario(facesCorreo,facytCorreo,faceCorreo,odontologiaCorreo,fcjpCorreo,ingieneriaCorreo,derechoCorreo):
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    
    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Facyt';"
    cur.execute(sqlquery7)
    Facyt=cur.fetchone()
    if(ValidarFecha(Facyt[0])):
        enviarCorreo("","")

   
    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Faces';"
    cur.execute(sqlquery7)
    Faces=cur.fetchone()
    if(ValidarFecha(Faces[0])):
        enviarCorreo("","")

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Face';"
    cur.execute(sqlquery7)
    Face=cur.fetchone()
    if(ValidarFecha(Face[0])):
        enviarCorreo("","")


    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Odontologia';"
    cur.execute(sqlquery7)
    Odontologia=cur.fetchone()
    if(ValidarFecha(Odontologia[0])):
        enviarCorreo("","")

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Fcjp';"
    cur.execute(sqlquery7)
    Fcjp=cur.fetchone()
    if(ValidarFecha(Fcjp[0])):
        enviarCorreo("","")

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Ingieneria';"
    cur.execute(sqlquery7)
    Ingieneria=cur.fetchone()
    if(ValidarFecha(Ingieneria[0])):
        enviarCorreo("","")

    sqlquery7 = "SELECT Fecha FROM FechaTope WHERE Facultad='Derecho';"
    cur.execute(sqlquery7)
    Derecho=cur.fetchone()
    if(ValidarFecha(Derecho[0])):
        enviarCorreo("","")
    
    
    conn.commit()
    cur.close()
    conn.close()




