import simplejson as json
import csv, operator
import sys
import types
import psycopg2
from microservices.scholar import main
import time
import datetime
from datetime import datetime
def Mensaje(aux,ErrorColum,data):
    switcher = {
        1: "Cedula",
        2: "primer_nombre",
        3: "segundo_nombre ",
        4: "primer_apellido  ",
        5: "segundo_apellido ",
        6: "sexo" ,
        7: "correo",
        8: "nacionalidad ",
        9: "tipo",
        10: "area de invetigacion ",
        11: "titulo",
        12: "Nivel",
        13: "otros estudios",
        14: "proyectos ",
        15: "premios ",
        16: "escalafon ",
        17: "Facultad "
    }
    if(ErrorColum==18):
        impr= "Error: el usuario no tiene permisos de insertar datos de otra facultad"
        
    else:
        if(ErrorColum==19):
            impr= "Error: el order de las columnas debe ser (ci,primer_nombre,segundo_nombre,primer_apellido,segundo_apellido,sexo,correo,Nacionalidad, Facultad,Tipo, AreaDeInvestigacion, titulo,Nivel, Otros_Estudios,Proyectos, Premios,Escalafon,Publicaciones)"
        else:
            impr= "Fila {} columna {}".format(aux,switcher[ErrorColum])
         
    data['Erros'].append({'error': impr})


def leerArchivoDocentes(NombreArchivo,user,data):
#conexion a la base de datos
    

    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    ""
    
    with open(NombreArchivo) as csvarchivo:
        #spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

        entrada = csv.DictReader(csvarchivo,delimiter=';')
       
        cont=2
        ListaDeCelulasDelSistema=[]
        ListatitulosSistema=[]
        ListaProyectosSistema=[]
        ListaOtroEstudioSistema=[]
        ListaPremiosSistema=[]
        ListaPublicacionSistema=[]
        ListaActuales=[]
        FilaInvalida=0;
        logico=1;
        queryCedulas = "SELECT cedula FROM Docente;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                 ListaDeCelulasDelSistema.append(int(row[0]));
        queryCedulas = "SELECT id,nomtitulo FROM titulo;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                 ListatitulosSistema.append(row);
        queryCedulas = "SELECT id,titulo FROM Proyecto;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                ListaProyectosSistema.append(row);
        queryCedulas = "SELECT id,nomtitulo FROM OtroEstudio;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                ListaOtroEstudioSistema.append(row);

        queryCedulas = "SELECT id,Nombre FROM Premio;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                ListaPremiosSistema.append(row);
        queryCedulas = "SELECT id,TituloPublicacion FROM Publicacion;"
        cur.execute(queryCedulas)
        rows=cur.fetchall()
        if(len(rows) > 0):
            for row in rows :
                 ListaPublicacionSistema.append(row);        
        orden=entrada.fieldnames
        for reg in entrada:
            
            if(len(reg)==19 and validadOrdenColum(orden)):
            #se valida cada uno de los campos

                if not (reg['ci'].isdigit()):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,1,data)
                if not (type(reg['primer_nombre'])==str and (reg['primer_nombre'].isalpha())):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,2,data)
                if not (type(reg['segundo_nombre'])==str and (reg['segundo_nombre'].isalpha())):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,3,data)
                if not (type(reg['primer_apellido'])==str and (reg['primer_apellido'].isalpha())):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,4,data)
                if not (type(reg['segundo_apellido'])==str and (reg['segundo_apellido'].isalpha())):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,5,data)
                if not (type(reg['sexo'])==str and (reg['sexo']=='F' or reg['sexo']=='M')):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,6,data)
                if not (type(reg['correo'])==str and (reg['correo'].find(".com") != -1 or reg['correo'].find(".ve") != -1 ) and reg['correo'].find("@") != -1):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,7,data) 
                if not (type(reg['Nacionalidad'])==str and (reg['Nacionalidad']=='V' or reg['Nacionalidad']=='E') ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,8,data)
                if not (type(reg['Tipo'])==str and ((reg['Tipo'].isalpha())) and ( reg['Tipo']=="Normal") or (  reg['Tipo']=="Contratado") or (reg['Tipo']=="Investigador" )):
                   
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,9,data)
                if not (type(reg['AreaDeInvestigacion'] )==str ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,10,data)
                if not (type(reg['titulo'])==str):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,11,data)
                if not (type(reg['Nivel'])==str):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,12,data)
                if not (type(reg['Otros_Estudios'])==str ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,13,data)
                if not (type(reg['Proyectos'])==str ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,14,data)
                if not (type(reg['Premios'])==str ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,15,data)
                if not (type(reg['Escalafon'])==str and ( reg['Escalafon']=="Instructor"  or reg['Escalafon']=="Asistente" or reg['Escalafon']=="Agregado"  or reg['Escalafon']=="Asociado"  or reg['Escalafon']=="Titular" )):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,16,data)
                if not (type(reg['Facultad'])==str and (reg['Facultad']=="Facyt" or reg['Facultad']=="Faces" or reg['Facultad']=="Fcs" or reg['Facultad']=="Fcjp" or reg['Facultad']=="Odontologia" or reg['Facultad']=="Ingieneria" or reg['Facultad']=="Face" or reg['Facultad']=="Ingineria" ) ):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,17,data)
                    logico=0;
             
                if not (vefificarFacultad(user,reg)):
                    FilaInvalida=-2
                    if(logico and FilaInvalida==0):
                        FilaInvalida= cont;
                        Mensaje(FilaInvalida,18,data) 
                if not (validadOrdenColum(orden)):
                    FilaInvalida= cont;
                    Mensaje(FilaInvalida,19,data)
            #si no hay ningun error se inserta 
                if(FilaInvalida == 0 ):

                    CedulaIngresada=int(reg['ci']) # se va registrando las cedula del docente

                    if(CedulaIngresada in ListaDeCelulasDelSistema):
                    # en caso que el docente este registrado en el sistema , se actualiza los campos mas importantes
                        if not (CedulaIngresada in ListaActuales):
                            if(reg['segundo_nombre']=="Ninguno"):
                                segundo=""
                            else:
                                segundo=reg['segundo_nombre']
                       
                            if(reg['segundo_apellido']=="Ninguno"):
                                segundoA=""
                            else:
                                segundoA=reg['segundo_apellido']
                    # se inserta la infomacion del docente
                            InsDocente = "  UPDATE Docente SET primernombre='{}',SegundoNombre='{}',primerapellido='{}',SegundoApellido='{}',Sexo='{}',correo='{}',Nacionalidad='{}',Facultad='{}',Tipo='{}',AreaDeInvestigacion='{}',Escalafon='{}',FechaActualizacion='{}' WHERE Cedula='{}';".format(reg['primer_nombre'],segundo,reg['primer_apellido'],segundoA,reg['sexo'],reg['correo'],reg['Nacionalidad'],reg['Facultad'],reg['Tipo'],reg['AreaDeInvestigacion'],reg['Escalafon'],time.strftime('%Y-%m-%d %H:%M:%S'),reg['ci'])
                            cur.execute(InsDocente)
                            actualizarPublicacion(reg,ListaPublicacionSistema)
                            actualizarTitulo(reg,cont,ListatitulosSistema)
                            actualizarProyectos(reg,ListaProyectosSistema)
                            actualizarPremios(reg,ListaPremiosSistema)
                            actualizarOtros(reg,ListaOtroEstudioSistema)
                        else:
                            "Error:El archivo ingresado contiene a 2 o mas docentes con la misma Cedula de indentidad"
                            FilaInvalida= cont;
                            

                    else:
                    # se descompone las cadena que contenga varios elmentos separados por coma
                        CadenaTitulo=reg['titulo'].split(",")
                        CadenaNivel=reg['Nivel'].split(",")
                        cadena2=reg['Otros_Estudios'].split(",")
                        cadena3=reg['Proyectos'].split(",")
                        cadena4=reg['Premios'].split(",")
                        cadena5=reg['Publicaciones'].split(",")
                    # se valida si tiene segundo nombre o segundo apellido
                        if(reg['segundo_nombre']=="Ninguno"):
                            segundo=""
                        else:
                            segundo=reg['segundo_nombre']
                       
                        if(reg['segundo_apellido']=="Ninguno"):
                            segundoA=""
                        else:
                            segundoA=reg['segundo_apellido']
                        # se inserta la infomacion del docente
                        InsDocente = "INSERT INTO Docente(Cedula,primernombre,SegundoNombre,primerapellido,SegundoApellido,Sexo,correo,Nacionalidad,Facultad,Tipo,AreaDeInvestigacion,Escalafon,FechaActualizacion) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}' );".format(reg['ci'],reg['primer_nombre'],segundo,reg['primer_apellido'],segundoA,reg['sexo'],reg['correo'],reg['Nacionalidad'],reg['Facultad'],reg['Tipo'],reg['AreaDeInvestigacion'],reg['Escalafon'],time.strftime('%Y-%m-%d %H:%M:%S'))
                        cur.execute(InsDocente)
                        #se obtine el ultimo id de titulo
                        ObtId = "SELECT id FROM titulo WHERE id=(SELECT MAX(id) from titulo);"
                        cur.execute(ObtId)
                        row=cur.fetchone()
                        if (row):
                            UltimoId= int(row[0])
                        else:
                            UltimoId=0;
                        i=0
                         #se Inserta en la la tabla titulo y en la relacion
                        while(i < len(CadenaTitulo) and i < len(CadenaNivel)  ):
                            if(CadenaNivel[i]=="Pregrado" or CadenaNivel[i]=="Postgrado" or CadenaNivel[i]=="Maestria" or CadenaNivel[i]=="Doctorado"):
                                aux=existeRelacion(ListatitulosSistema,CadenaTitulo[i])
                                if(aux):
                                    sqlquery3 = "INSERT INTO DocenteTieneTitulo(CedulaPersona,IdTitulo) VALUES ('{}','{}' );".format(reg['ci'],aux)
                                    cur.execute(sqlquery3)

                                else:
                                    UltimoId=(UltimoId)+1
                                    sqlquery3 = "INSERT INTO titulo(id,nomtitulo,Nivel,FechaActualizacion) VALUES ('{}','{}','{}','{}' );".format(UltimoId,CadenaTitulo[i],CadenaNivel[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                                    cur.execute(sqlquery3)
                                    sqlquery3 = "INSERT INTO DocenteTieneTitulo(CedulaPersona,IdTitulo) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                                    cur.execute(sqlquery3)
                                    ListatitulosSistema.append((UltimoId,CadenaTitulo[i]))
                            else:

                                FilaInvalida= cont;
                                Mensaje(FilaInvalida,12,data)+','
                            i=i+1
                        #se obtine el ultimo id de OtroEstudio
                        ObtId = "SELECT id FROM OtroEstudio WHERE id=(SELECT MAX(id) from OtroEstudio);"
                        cur.execute(ObtId)
                        row=cur.fetchone()
                        if (row):
                            UltimoId= int(row[0])
                        else:
                            UltimoId=0;
                        i=0
                         #se Inserta en la la tabla OtroEstudio y en la relacion
                        while(i < len(cadena2) and cadena2[i] !="Ninguno" ):
                            aux=existeRelacion(ListaOtroEstudioSistema,cadena2[i])
                            if(aux):
                                sqlquery3 = "INSERT INTO DocenteRealizaOtroEstudio(CedulaPersona,IdOtroEstudio) VALUES ('{}','{}' );".format(reg['ci'],aux)
                                cur.execute(sqlquery3)
                            else:
                                UltimoId=(UltimoId)+1
                                sqlquery4 = "INSERT INTO OtroEstudio(id,nomtitulo,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena2[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                                cur.execute(sqlquery4)
                                sqlquery3 = "INSERT INTO DocenteRealizaOtroEstudio(CedulaPersona,IdOtroEstudio) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                                cur.execute(sqlquery3)
                                ListaOtroEstudioSistema.append((UltimoId,cadena2[i]))
                            i=i+1
                        #se obtine el ultimo id de Proyecto
                        ObtId = "SELECT id FROM Proyecto WHERE id=(SELECT MAX(id) from Proyecto);"
                        cur.execute(ObtId)
                        row=cur.fetchone()
                        if (row):
                            UltimoId= int(row[0])
                        else:
                            UltimoId=0
                        i=0
                        #se Inserta en la la tabla Proyecto y en la relacion
                        while(i < len(cadena3) and cadena3[i] !="Ninguno" ):
                            aux=existeRelacion(ListaProyectosSistema,cadena3[i])
                            if(aux):
                                sqlquery3 = "INSERT INTO DocenteParticipaProyecto(CedulaPersona,IdProyecto) VALUES ('{}','{}' );".format(reg['ci'],aux)
                                cur.execute(sqlquery3)
                            else:
                                UltimoId=(UltimoId)+1
                                sqlquery5 = "INSERT INTO Proyecto(id,titulo,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena3[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                                cur.execute(sqlquery5)
                                sqlquery3 = "INSERT INTO DocenteParticipaProyecto(CedulaPersona,IdProyecto) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                                cur.execute(sqlquery3)
                                ListaProyectosSistema.append((UltimoId,cadena3[i]))
                            i=i+1
                        
                         #se obtine el ultimo id de Premio    
                        ObtId = "SELECT id FROM Premio WHERE id=(SELECT MAX(id) from Premio);"
                        cur.execute(ObtId)
                        row=cur.fetchone()
                        if (row):
                            UltimoId= int(row[0])
                        else:
                            UltimoId=0
                        i=0
                        #se Inserta en la la tabla Premio y en la relacion
                        while(i < len(cadena4)  and cadena4[i] !="Ninguno" ):
                            aux=existeRelacion(ListaPremiosSistema,cadena4[i])
                            if(aux):
                                sqlquery3 = "INSERT INTO DocenteTienePremio(CedulaPersona,IdPremio) VALUES ('{}','{}' );".format(reg['ci'],aux)
                                cur.execute(sqlquery3)
                            else:
                                UltimoId=(UltimoId)+1
                                sqlquery6 = "INSERT INTO Premio(id,Nombre,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena4[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                                cur.execute(sqlquery6)
                                sqlquery3 = "INSERT INTO DocenteTienePremio(CedulaPersona,IdPremio) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                                cur.execute(sqlquery3)
                                ListaPremiosSistema.append((UltimoId,cadena4[i]))
                            i=i+1
                        #se obtine el ultimo id de Publicacion
                        ObtId = "SELECT id FROM Publicacion WHERE id=(SELECT MAX(id) from Publicacion);"
                        cur.execute(ObtId)
                        row=cur.fetchone()
                        if (row):
                            UltimoId= int(row[0])
                        else:
                            UltimoId=0
                        i=0
                         #se Inserta en la la tabla Publicacion y en la relacion
                        while(i < len(cadena5)  and cadena5[i] !="Ninguno" ):
                            aux=existeRelacion(ListaPublicacionSistema,cadena5[i])
                            if(aux):
                                sqlquery3 = "INSERT INTO DocenteTienePublicacion(CedulaPersona,IdPublicacion) VALUES ('{}','{}' );".format(reg['ci'],aux)
                                cur.execute(sqlquery3)
                            else:
                                UltimoId=(UltimoId)+1
                                sqlquery6 = "INSERT INTO Publicacion(Id,TituloPublicacion,UrlCitacion,UrlPublicacion,NumeroCitaciones,FechaActualizacion) VALUES ('{}','{}','{}','{}','{}','{}');".format(UltimoId,cadena5[i],"no tiene link","no tiene link",0,time.strftime('%Y-%m-%d %H:%M:%S'))
                                cur.execute(sqlquery6)
                                sqlquery3 = "INSERT INTO DocenteTienePublicacion(CedulaPersona,IdPublicacion) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                                cur.execute(sqlquery3)
                                ListaPublicacionSistema.append((UltimoId,cadena5[i]))
                            i=i+1
                        #se registra el nuevo docente
                        ListaDeCelulasDelSistema.append(int(reg['ci']))
                
            else:
                FilaInvalida=-1
            if(validadOrdenColum(orden)):   
                ListaActuales.append(int(reg['ci']))            
            cont=cont+1

        

    if(FilaInvalida == 0 ):
        conn.commit()
        cur.close()
        conn.close()
        return "El Archivo csv ha sido procesado con exito!!!"
    else:
        conn.rollback()
        if(FilaInvalida == -1 ):
            return "Error: formato invalido"
        else:
            if not (validadOrdenColum(orden)):
                return "Error: formato invalido"
            else:
                if(FilaInvalida == -2):
                    return "Error a procesar el archivo : este usuario no tiene permiso para ingresar informacion de otra facultad"
                else:
                    return "Error a procesar el archivo. Por favor revise el pdf LISTA_ERRORES para conocer los errores del archivo ingresado al sistema" 
        
def actualizarTitulo(reg,cont,ListatitulosSistema):
    ListaTilulos=[]
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    MensajeE=""
    queryTitulos = "SELECT t.nomtitulo FROM titulo T ,DocenteTieneTitulo R WHERE R.CedulaPersona={} and R.IdTitulo=T.Id;".format(reg['ci'])
    cur.execute(queryTitulos)
    rows=cur.fetchall()
    if(len(rows) > 0):
            for row in rows :
                 ListaTilulos.append(row[0]);
   
    CadenaTitulo=reg['titulo'].split(",")
    CadenaNivel=reg['Nivel'].split(",")
    ObtId = "SELECT id FROM titulo WHERE id=(SELECT MAX(id) from titulo);"
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        UltimoId= int(row[0])
    else:
        UltimoId=0
    i=0
    FilaInvalida=0
     #se Inserta en la la tabla Publicacion y en la relacion
    while(i < len(CadenaTitulo) and i < len(CadenaNivel)  and FilaInvalida==0 ):
        if(CadenaNivel[i]=="Pregrado" or CadenaNivel[i]=="Postgrado" or CadenaNivel[i]=="Maestria" or CadenaNivel[i]=="Doctorado"):
            if not (CadenaTitulo[i] in ListaTilulos):
                aux=existeRelacion(ListatitulosSistema,CadenaTitulo[i])
                if(aux):
                    sqlquery3 = "INSERT INTO DocenteTieneTitulo(CedulaPersona,IdTitulo) VALUES ('{}','{}' );".format(reg['ci'],aux)
                    cur.execute(sqlquery3)

                else:
                    UltimoId=(UltimoId)+1
                    sqlquery3 = "INSERT INTO titulo(id,nomtitulo,Nivel,FechaActualizacion) VALUES ('{}','{}','{}','{}' );".format(UltimoId,CadenaTitulo[i],CadenaNivel[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                    cur.execute(sqlquery3)
                    sqlquery3 = "INSERT INTO DocenteTieneTitulo(CedulaPersona,IdTitulo) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                    cur.execute(sqlquery3)
                    ListatitulosSistema.append((UltimoId,CadenaTitulo[i]))
                ListaTilulos.append(CadenaTitulo[i]);
        else:
            FilaInvalida= cont;
            MensajeE=Mensaje(FilaInvalida,12,data)+','
        i=i+1
    if(FilaInvalida==0):
        conn.commit()
    return(MensajeE)

def actualizarPublicacion(reg,ListaPublicacionSistema):
    ListaPublicacion=[]
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    queryCedulas = "SELECT TituloPublicacion FROM Publicacion P, DocenteTienePublicacion R WHERE(R.CedulaPersona={} and P.Id=R.IdPublicacion);".format(reg['ci'])
    cur.execute(queryCedulas)
    rows=cur.fetchall()
   
    if(len(rows) > 0):
            for row in rows :
                
                ListaPublicacion.append(row[0]);
   
    cadena5=reg['Publicaciones'].split(",")
    ObtId = "SELECT id FROM Publicacion WHERE id=(SELECT MAX(id) from Publicacion);"
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        UltimoId= int(row[0])
    else:
        UltimoId=0
    i=0
     #se Inserta en la la tabla Publicacion y en la relacion
    
    while(i < len(cadena5)  and cadena5[i] !="Ninguno" ):
        if not( cadena5[i] in ListaPublicacion):
            aux=existeRelacion(ListaPublicacionSistema,cadena5[i])
            if(aux):
                sqlquery3 = "INSERT INTO DocenteTienePublicacion(CedulaPersona,IdPublicacion) VALUES ('{}','{}' );".format(reg['ci'],aux)
                cur.execute(sqlquery3)
            else:
                UltimoId=(UltimoId)+1
                sqlquery6 = "INSERT INTO Publicacion(Id,TituloPublicacion,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena5[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                cur.execute(sqlquery6)
                sqlquery3 = "INSERT INTO DocenteTienePublicacion(CedulaPersona,IdPublicacion) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                cur.execute(sqlquery3)
                ListaPublicacionSistema.append((UltimoId,cadena5[i]))
            
            ListaPublicacion.append(cadena5[i])
        i=i+1
    
    conn.commit()

def actualizarProyectos(reg,ListaProyectosSistema):
    Lista=[]
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    MensajeE=""
    queryTitulos = "SELECT t.titulo FROM Proyecto T ,DocenteParticipaProyecto R WHERE R.CedulaPersona={} and R.IdProyecto=T.Id;".format(reg['ci'])
    
    cur.execute(queryTitulos)

    rows=cur.fetchall()

    if(len(rows) > 0):
            for row in rows :
                 Lista.append(row[0]);
   
    cadena3=reg['Proyectos'].split(",")
    ObtId = "SELECT id FROM Proyecto WHERE id=(SELECT MAX(id) from Proyecto);"
    cur.execute(ObtId)
    row=cur.fetchone()

    if (row):
        UltimoId= int(row[0])
    else:
        UltimoId=0
    i=0
    FilaInvalida=0
     #se Inserta en la la tabla Publicacion y en la relacion
    while(i < len(cadena3) and cadena3[i] !="Ninguno" ):
        if not(cadena3[i] in Lista):
            aux=existeRelacion(ListaProyectosSistema,cadena3[i])
            if(aux):
                sqlquery3 = "INSERT INTO DocenteParticipaProyecto(CedulaPersona,IdProyecto) VALUES ('{}','{}' );".format(reg['ci'],aux)
                cur.execute(sqlquery3)
            else:
                UltimoId=(UltimoId)+1
                sqlquery5 = "INSERT INTO Proyecto(id,titulo,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena3[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                cur.execute(sqlquery5)
                sqlquery3 = "INSERT INTO DocenteParticipaProyecto(CedulaPersona,IdProyecto) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                cur.execute(sqlquery3)
                ListaProyectosSistema.append((UltimoId,cadena3[i]))
            
            Lista.append(cadena3[i]);
        i=i+1
    conn.commit()
    
def actualizarPremios(reg,ListaPremiosSistema):
    Lista=[]
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    MensajeE=""
    queryTitulos = "SELECT t.Nombre FROM Premio T ,DocenteTienePremio R WHERE R.CedulaPersona={} and R.IdPremio=T.Id;".format(reg['ci'])
    cur.execute(queryTitulos)
    rows=cur.fetchall()
    if(len(rows) > 0):
            for row in rows :
                 Lista.append(row[0]);
   
    cadena4=reg['Premios'].split(",")
    ObtId = "SELECT id FROM Premio WHERE id=(SELECT MAX(id) from Premio);"
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        UltimoId= int(row[0])
    else:
        UltimoId=0
    i=0
    FilaInvalida=0
     #se Inserta en la la tabla Publicacion y en la relacion

    while(i < len(cadena4) and cadena4[i] !="Ninguno" ):
        if not(cadena4[i] in Lista):
            aux=existeRelacion(ListaPremiosSistema,cadena4[i])
            if(aux):
                sqlquery3 = "INSERT INTO DocenteTienePremio(CedulaPersona,IdPremio) VALUES ('{}','{}' );".format(reg['ci'],aux)
                cur.execute(sqlquery3)
            else:
                UltimoId=(UltimoId)+1
                sqlquery6 = "INSERT INTO Premio(id,Nombre,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena4[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                cur.execute(sqlquery6)
                sqlquery3 = "INSERT INTO DocenteTienePremio(CedulaPersona,IdPremio) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                cur.execute(sqlquery3)
                ListaPremiosSistema.append((UltimoId,cadena4[i]))
        i=i+1
    conn.commit()

def actualizarOtros(reg,ListaOtroEstudioSistema):
    Lista=[]
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    MensajeE=""
    queryTitulos = "SELECT t.Nomtitulo FROM OtroEstudio T ,DocenteRealizaOtroEstudio R WHERE R.CedulaPersona={} and R.IdOtroEstudio=T.Id;".format(reg['ci'])
    cur.execute(queryTitulos)
    rows=cur.fetchall()
    if(len(rows) > 0):
            for row in rows :
                 Lista.append(row[0]);
   
    
    ObtId = "SELECT id FROM OtroEstudio WHERE id=(SELECT MAX(id) from OtroEstudio);"
    cur.execute(ObtId)
    row=cur.fetchone()
    if (row):
        UltimoId= int(row[0])
    else:
        UltimoId=0
    i=0
    FilaInvalida=0
     #se Inserta en la la tabla Publicacion y en la relacion
    cadena2=reg['Otros_Estudios'].split(",")
    while(i < len(cadena2) and cadena2[i] !="Ninguno" ):
        if not(cadena2[i] in Lista):
            aux=existeRelacion(ListaOtroEstudioSistema,cadena2[i])
            if(aux):
                sqlquery3 = "INSERT INTO DocenteRealizaOtroEstudio(CedulaPersona,IdOtroEstudio) VALUES ('{}','{}' );".format(reg['ci'],aux)
                cur.execute(sqlquery3)
            else:
                UltimoId=(UltimoId)+1
                sqlquery4 = "INSERT INTO OtroEstudio(id,nomtitulo,FechaActualizacion) VALUES ('{}','{}','{}');".format(UltimoId,cadena2[i],time.strftime('%Y-%m-%d %H:%M:%S'))
                cur.execute(sqlquery4)
                sqlquery3 = "INSERT INTO DocenteRealizaOtroEstudio(CedulaPersona,IdOtroEstudio) VALUES ('{}','{}' );".format(reg['ci'],UltimoId)
                cur.execute(sqlquery3)
                ListaOtroEstudioSistema.append((UltimoId,cadena2[i]))
            
            Lista.append(cadena2[i]);
        i=i+1
    conn.commit()


def vefificarFacultad(user, reg):
    logico=True
    if(user=='Facyt_docente' and reg['Facultad'] !='Facyt' ):
        logico=False
    else:
        if(user=='Faces_docente' and reg['Facultad'] !='Faces' ):
            logico=False
        else:
            if(user=='Face_docente' and reg['Facultad'] !='Face' ):
                logico=False
            else:
                if(user=='Ingieneria_docente' and reg['Facultad'] !='Ingieneria' ):
                    logico=False
                else:
                    if(user=='Odontologia_docente' and reg['Facultad'] !='Odontologia' ):
                        logico=False
                    else:
                        if(user=='Fcjp_docente' and reg['Facultad'] !='Fcjp' ):
                            logico=False
                        else:
                            if(user=='Fcs_docente' and reg['Facultad'] !='Fcs' ):
                                logico=False
    if(user=='vicerrector'):
        logico=True


    return logico

def validadOrdenColum(fieldnames):
    try:
        logico=True
        if(fieldnames[0]!="ci"):
            logico=False
        if(fieldnames[1]!="primer_nombre"):
            logico=False
        if(fieldnames[2]!="segundo_nombre"):
            logico=False
        if(fieldnames[3]!="primer_apellido"):
            logico=False
        if(fieldnames[4]!="segundo_apellido"):
            logico=False
        if(fieldnames[5]!="sexo"):
            logico=False
        if(fieldnames[6]!="correo"):
            logico=False
        if(fieldnames[7]!="Nacionalidad"):
            logico=False
        if(fieldnames[8]!="Facultad"):
            logico=False
        if(fieldnames[9]!="Tipo"):
            logico=False
        if(fieldnames[10]!="AreaDeInvestigacion"):
            logico=False
        if(fieldnames[11]!="titulo"):
            logico=False
        if(fieldnames[12]!="Nivel"):
            logico=False 
        if(fieldnames[14]!="Otros_Estudios"):
            logico=False
        if(fieldnames[16]!="Proyectos"):
            logico=False 
        if(fieldnames[18]!="Premios"):
            logico=False 
        if(fieldnames[20]!="Escalafon"):
            logico=False
        if(fieldnames[21]!="Publicaciones"):
            logico=False
        return(logico)
    except:
        return(False)

def existeRelacion(lista,valor):
    logico=0
    for item in lista : 
        if(logico==0):
            if(item[1]==valor):
                logico=int(item[0])

    return logico