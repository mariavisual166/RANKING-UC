from flask_restful import abort, Resource, reqparse
import simplejson as json
from psycopg2 import DatabaseError
from textwrap import dedent
from common.BD import BD
from flask import make_response, jsonify, request
from datetime import datetime
#base  de datos
import psycopg2


class TeachersInsertInitial(BD, Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    # Postgres
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
   
    PSQL_PASS = "0000"
    PSQL_DB   = "docente"
    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
    conn = psycopg2.connect(connstr)
    cur = conn.cursor()
    def get(self):
        try:
            # consultar OtroEstudio
            resultOtroEstudio = self.queryAll(dedent("""SELECT O.Id As codigo ,O.Nomtitulo FROM OtroEstudio O"""))

            # relacion de otrosEstudios
            relacionDocenteReliazoOtroEstudio = self.queryAll(dedent("""\
                SELECT d.cedula as docente , o.id as otroestudio
                FROM docente as d
                INNER JOIN docenterealizaotroestudio dp
                ON (d.cedula = dp.cedulapersona)
                INNER JOIN otroestudio as o
                ON (dp.idotroestudio = o.id)
                """))
            # consultar Publicaciones
            resultPublicacion = self.queryAll(dedent("""\
                SELECT P.Id As codigo, P.UrlCitacion, P.TituloPublicacion, P.UrlPublicacion 
                FROM Publicacion P"""))

            relacionDocenteTienePublicacion = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as publicacion, p.numerocitaciones 
                FROM docente AS d
                INNER JOIN docentetienepublicacion AS dp
                ON(d.cedula = dp.cedulapersona)
                INNER JOIN publicacion AS p
                ON(dp.idpublicacion = p.id)"""))
            # consultar Proyecto
            resultProyecto = self.queryAll(dedent("""\
                SELECT P.Id AS codigo,P.titulo 
                FROM Proyecto P"""))

            relacionDocenteParticipaProyecto = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as proyecto
                FROM docente AS d
                INNER JOIN docenteparticipaproyecto AS dp
                ON(d.cedula = dp.cedulapersona)
                INNER JOIN proyecto AS p
                ON(dp.idproyecto = p.id)"""))
            # consultar Titulos
            resultTitulo = self.queryAll(dedent("""\
                SELECT P.Id AS codigo,P.Nomtitulo FROM Titulo P"""))

            relacionDocenteTieneTitulo = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as titulo, p.nivel 
                FROM docente AS d
                INNER JOIN docentetienetitulo AS dp
                ON(d.cedula = dp.cedulapersona)
                INNER JOIN titulo AS p
                ON(dp.idtitulo = p.id)"""))
             # consultar Premios
            resultPremio = self.queryAll(dedent("""\
                SELECT P.Id as Codigo,P.Nombre FROM Premio P"""))

            relacionDocenteTienePremio = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as premio
                FROM docente AS d
                INNER JOIN docentetienepremio AS dp
                ON(d.cedula = dp.cedulapersona)
                INNER JOIN premio AS p
                ON(dp.idpremio = p.id)"""))

            # consultar docentes
            resultTeacher = self.queryAll(dedent("""\
            SELECT Cedula, primernombre, SegundoNombre, primerapellido, SegundoApellido, Sexo, correo, Nacionalidad, Facultad, Tipo,AreaDeInvestigacion,Escalafon 
            FROM docente"""))
            
               
            response = {
                "dim-docente": {"items": resultTeacher},
                "dim-otroestudio": {"items": resultOtroEstudio}, 
                "dim-publicacion": {"items":resultPublicacion},
                "dim-proyecto": {"items":resultProyecto},
                "dim-titulo": {"items":resultTitulo},
                "dim-premio": {"items":resultPremio},
                "hechos-docente-otroestudio": {"items": relacionDocenteReliazoOtroEstudio},
                "hechos-docente-publicacion": {"items": relacionDocenteTienePublicacion},
                "hechos-docente-proyecto": {"items": relacionDocenteParticipaProyecto},
                "hechos-docente-titulo": {"items": relacionDocenteTieneTitulo},
                "hechos-docente-premio": {"items": relacionDocenteTienePremio}               
                        
            }  
        except DatabaseError as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

        return json.dumps(response), 200, { 'Access-Control-Allow-Origin': '*' }

        
        
class TeacherstUpdate(BD, Resource):
    representations = {'application/json': make_response}
    parser = reqparse.RequestParser()
    
    def get(self, date_update):

        try:
            date_update = datetime.strptime(date_update, '%Y-%m-%d %H:%M:%S')
            resultOtroEstudio = self.queryAll(dedent("""SELECT O.Id As codigo ,O.Nomtitulo FROM OtroEstudio O WHERE O.FechaActualizacion>= %s"""), [date_update])

            # relacion de otrosEstudios
            relacionDocenteReliazoOtroEstudio = self.queryAll(dedent("""\
                SELECT d.cedula as docente , o.id as otroestudio
                FROM docente as d
                INNER JOIN docenterealizaotroestudio dp
                ON (d.cedula = dp.cedulapersona)
                INNER JOIN otroestudio as o
                ON (dp.idotroestudio = o.id  ) WHERE  o.FechaActualizacion>= %s or d.FechaActualizacion>= %s
                """),[date_update,date_update])
            # consultar Publicaciones
            resultPublicacion = self.queryAll(dedent("""\
                SELECT P.Id As codigo, P.UrlCitacion, P.TituloPublicacion, P.UrlPublicacion 
                FROM Publicacion P WHERE P.FechaActualizacion>= %s"""), [date_update])

            relacionDocenteTienePublicacion = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as publicacion, p.numerocitaciones 
                FROM docente AS d
                INNER JOIN docentetienepublicacion AS dp
                ON(d.cedula = dp.cedulapersona )
                INNER JOIN publicacion AS p
                ON(dp.idpublicacion = p.id  ) WHERE d.FechaActualizacion>= %s or p.FechaActualizacion>= %s"""),[date_update,date_update])
            # consultar Proyecto
            resultProyecto = self.queryAll(dedent("""\
                SELECT P.Id AS codigo,P.titulo 
                FROM Proyecto P WHERE P.FechaActualizacion>= %s"""), [date_update])


            relacionDocenteParticipaProyecto = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as proyecto
                FROM docente AS d
                INNER JOIN docenteparticipaproyecto AS dp
                ON(d.cedula = dp.cedulapersona  )
                INNER JOIN proyecto AS p
                ON(dp.idproyecto = p.id  ) WHERE p.FechaActualizacion>= %s or d.FechaActualizacion>= %s"""),[date_update,date_update])
            # consultar Titulos
            resultTitulo = self.queryAll(dedent("""\
                SELECT P.Id AS codigo,P.Nomtitulo FROM Titulo P WHERE P.FechaActualizacion>= %s"""), [date_update])

            relacionDocenteTieneTitulo = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as titulo, p.nivel 
                FROM docente AS d
                INNER JOIN docentetienetitulo AS dp
                ON(d.cedula = dp.cedulapersona )
                INNER JOIN titulo AS p
                ON(dp.idtitulo = p.id ) WHERE d.FechaActualizacion>= %s or p.FechaActualizacion>= %s"""),[date_update,date_update])
             # consultar Premios
            resultPremio = self.queryAll(dedent("""\
                SELECT P.Id as Codigo,P.Nombre FROM Premio P WHERE P.FechaActualizacion>= %s"""), [date_update])

            relacionDocenteTienePremio = self.queryAll(dedent("""\
                SELECT d.cedula as docente, p.id as premio
                FROM docente AS d
                INNER JOIN docentetienepremio AS dp
                ON(d.cedula = dp.cedulapersona  )
                INNER JOIN premio AS p
                ON(dp.idpremio = p.id ) WHERE p.FechaActualizacion>= %s or d.FechaActualizacion>= %s"""), [date_update,date_update])

           
            
            resultTeacher = self.queryAll(dedent("""\
            SELECT Cedula, primernombre, SegundoNombre, primerapellido, SegundoApellido, Sexo, correo, Nacionalidad, Facultad, Tipo,AreaDeInvestigacion,Escalafon 
            FROM docente WHERE FechaActualizacion >= %s"""), [date_update])
           
            response = {
                "dim-docente": {"items": resultTeacher},
                "dim-otroestudio": {"items": resultOtroEstudio}, 
                "dim-publicacion": {"items":resultPublicacion},
                "dim-proyecto": {"items":resultProyecto},
                "dim-titulo": {"items":resultTitulo},
                "dim-premio": {"items":resultPremio},
                "hechos-docente-otroestudio": {"items": relacionDocenteReliazoOtroEstudio},
                "hechos-docente-publicacion": {"items": relacionDocenteTienePublicacion},
                "hechos-docente-proyecto": {"items": relacionDocenteParticipaProyecto},
                "hechos-docente-titulo": {"items": relacionDocenteTieneTitulo},
                "hechos-docente-premio": {"items": relacionDocenteTienePremio}               
                        
            }  
            
        except DatabaseError as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))
        except Exception as e:
            abort(500, message="{0}:{1}".format(e.__class__.__name__, e.__str__()))

        return jsonify(response), 200, { 'Access-Control-Allow-Origin': '*' }



    

