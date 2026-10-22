from datetime import datetime, date
from flask import flash
from config.mysqlconnection import connectToMySQL

BASE_DE_DATOS = 'db_eventos'

class Evento:
    def __init__(self, datos):
        self.id = datos.get('id')
        self.nombre_evento = datos.get('nombre_evento')
        self.ubicacion = datos.get('ubicacion')
        self.fecha_evento = datos.get('fecha_evento')
        self.detalles = datos.get('detalles')
        self.usuario_id = datos.get('usuario_id')
        self.nombre_anfitrion = datos.get('nombre_anfitrion')
        self.apellido_anfitrion = datos.get('apellido_anfitrion')
        self.fecha_creacion = datos.get('created_at')
        self.fecha_actualizacion = datos.get('updated_at')

    @classmethod
    def obtener_todos_con_anfitrion(cls):
        consulta = """
            SELECT e.id, e.event_name AS nombre_evento, e.location AS ubicacion, 
                   e.event_date AS fecha_evento, e.details AS detalles, e.user_id AS usuario_id,
                   e.created_at, e.updated_at,
                   u.first_name AS nombre_anfitrion, u.last_name AS apellido_anfitrion
            FROM events e
            JOIN users u ON e.user_id = u.id
            ORDER BY e.event_date ASC;
        """
        resultados = connectToMySQL(BASE_DE_DATOS).query_db(consulta)
        eventos = []
        if resultados:
            for fila in resultados:
                eventos.append(cls(fila))
        return eventos

    @classmethod
    def obtener_ids_eventos_unidos(cls, datos):
        consulta = "SELECT event_id FROM users_events WHERE user_id = %(usuario_id)s;"
        resultados = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)
        ids_unidos = []
        if resultados:
            for fila in resultados:
                ids_unidos.append(fila['event_id'])
        return ids_unidos

    @classmethod
    def guardar(cls, datos):
        consulta = """
            INSERT INTO events (event_name, location, event_date, details, user_id)
            VALUES (%(nombre_evento)s, %(ubicacion)s, %(fecha_evento)s, %(detalles)s, %(usuario_id)s);
        """
        id_evento = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)
        # El anfitrión se une automáticamente al evento
        cls.unirse({'usuario_id': datos['usuario_id'], 'evento_id': id_evento})
        return id_evento

    @classmethod
    def obtener_por_id(cls, datos):
        consulta = """
            SELECT e.id, e.event_name AS nombre_evento, e.location AS ubicacion, 
                   e.event_date AS fecha_evento, e.details AS detalles, e.user_id AS usuario_id,
                   e.created_at, e.updated_at,
                   u.first_name AS nombre_anfitrion, u.last_name AS apellido_anfitrion
            FROM events e
            JOIN users u ON e.user_id = u.id
            WHERE e.id = %(id)s;
        """
        resultado = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)
        if not resultado or len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def actualizar(cls, datos):
        consulta = """
            UPDATE events
            SET event_name = %(nombre_evento)s, location = %(ubicacion)s,
                event_date = %(fecha_evento)s, details = %(detalles)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def eliminar(cls, datos):
        consulta = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def unirse(cls, datos):
        consulta = "INSERT IGNORE INTO users_events (user_id, event_id) VALUES (%(usuario_id)s, %(evento_id)s);"
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def abandonar(cls, datos):
        consulta = "DELETE FROM users_events WHERE user_id = %(usuario_id)s AND event_id = %(evento_id)s;"
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def obtener_asistentes(cls, datos):
        consulta = """
            SELECT u.first_name AS nombre, u.last_name AS apellido
            FROM users u
            JOIN users_events ue ON u.id = ue.user_id
            WHERE ue.event_id = %(evento_id)s;
        """
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @staticmethod
    def validar_evento(datos):
        es_valido = True
        if not datos.get('nombre_evento', '').strip() or not datos.get('ubicacion', '').strip() or \
           not datos.get('fecha_evento', '').strip() or not datos.get('detalles', '').strip():
            flash('Todos los campos son obligatorios', 'error_evento')
            return False
        try:
            fecha_evento = datetime.strptime(datos.get('fecha_evento'), '%Y-%m-%d').date()
            if fecha_evento <= date.today():
                flash('La fecha debe estar en el futuro', 'error_evento')
                es_valido = False
        except ValueError:
            flash('Ingrese una fecha válida', 'error_evento')
            es_valido = False
        return es_valido