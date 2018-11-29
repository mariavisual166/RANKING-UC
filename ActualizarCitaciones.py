import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.scholar import main
import time
import datetime
def Actualizar():
	
	PSQL_HOST = "localhost"
	PSQL_PORT = "5432"
	PSQL_USER = "postgres"
	PSQL_PASS = "0000"
	PSQL_DB   = "docente"
	connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
	conn = psycopg2.connect(connstr)
	cur = conn.cursor()

	if((int(time.strftime("%d"))==11 or int(time.strftime("%d"))==10 or int(time.strftime("%d"))==20) and int(time.strftime("%M"))==27 and ( int(time.strftime("%S"))==10 or int(time.strftime("%S"))==12 ) and int(time.strftime("%H"))==20 ):
		
		ListaDeNombresDelSistema=[]
		ListaDePirmerApellidoDelSistema=[]
		ListaDePublicaciones=[]
		ListaAux=[]
		sqlquery7 = "SELECT p.TituloPublicacion,d.primerNombre,d.primerapellido FROM Docente d ,Publicacion p ,DocenteTienePublicacion t where t.IdPublicacion=P.id and t.CedulaPersona=d.Cedula ;"
		cur.execute(sqlquery7)
		rows=cur.fetchall()
		if(len(rows) > 0):
			for row in rows:
				ListaDePublicaciones.append(row[0]);
				ListaDeNombresDelSistema.append(row[1]);
				ListaDePirmerApellidoDelSistema.append(row[2]);
		j=0
	
		while j < len(ListaDePublicaciones) :
			
			autor=ListaDeNombresDelSistema[j]+" "+ListaDePirmerApellidoDelSistema[j]
			#V[0]= Numero de publicaciones 
			#V[1]= URL de citaciones 
			#V[1]= URL de la Publicacion 
			#ListaDePublicaciones[j]=Titulo de la publicacion 
			#
			V=main(autor,ListaDePublicaciones[j])
			if(len(V)):
				sqlquery10 = "UPDATE Publicacion SET NumeroCitaciones='{}',UrlCitacion='{}',UrlPublicacion='{}' WHERE TituloPublicacion='{}';".format(int(V[0]),V[1],V[3],ListaDePublicaciones[j])
				cur.execute(sqlquery10)
			#sqlquery8 = "INSERT INTO Publicacion(CedulaAutor,NumeroCitaciones,UrlCitacion,TituloPublicacion,UrlPublicacion,FechaActualizacion ) VALUES ('{}','{}','{}','{}','{}','{}' );".format(ListaDePublicaciones[j],int(V[i]),V[i+1],V[i+2],V[i+3],time.strftime('%Y-%m-%d'))
			#cur.execute(sqlquery8)
			
			j=j+1
		print("Se realizo una Actualizacion..")
		conn.commit() 
		cur.close()
		conn.close()

def main_():
	print("corriendo Actualizacion..")
	while (True):
		Actualizar()
		time.sleep(0.50)

main_()