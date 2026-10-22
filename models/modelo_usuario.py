import re
from flask import flash
from config.mysqlconnection import connectToMySQL

EXPRESION_REGULAR_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
BASE_DE_DATOS = 'db_eventos'

class Usuario:
    def __init__(self, datos):
        self.id = datos.get('id')
        self.nombre = datos.get('nombre')
        self.apellido = datos.get('apellido')
        self.correo = datos.get('correo')
        self.contrasena = datos.get('contrasena')
        self.fecha_creacion = datos.get('created_at')
        self.fecha_actualizacion = datos.get('updated_at')

    @classmethod
    def guardar(cls, datos):
        consulta = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(nombre)s, %(apellido)s, %(correo)s, %(contrasena)s);
        """
        return connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)

    @classmethod
    def obtener_por_correo(cls, datos):
        consulta = "SELECT * FROM users WHERE email = %(correo)s;"
        resultado = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)
        if not resultado or len(resultado) < 1:
            return False
        
        # Mapear columnas de la BD al constructor del modelo
        datos_usuario = resultado[0]
        datos_usuario['nombre'] = datos_usuario.pop('first_name', None)
        datos_usuario['apellido'] = datos_usuario.pop('last_name', None)
        datos_usuario['correo'] = datos_usuario.pop('email', None)
        datos_usuario['contrasena'] = datos_usuario.pop('password', None)
        
        return cls(datos_usuario)

    @classmethod
    def obtener_por_id(cls, datos):
        consulta = "SELECT * FROM users WHERE id = %(id)s;"
        resultado = connectToMySQL(BASE_DE_DATOS).query_db(consulta, datos)
        if not resultado or len(resultado) < 1:
            return False
        
        datos_usuario = resultado[0]
        datos_usuario['nombre'] = datos_usuario.pop('first_name', None)
        datos_usuario['apellido'] = datos_usuario.pop('last_name', None)
        datos_usuario['correo'] = datos_usuario.pop('email', None)
        datos_usuario['contrasena'] = datos_usuario.pop('password', None)
        
        return cls(datos_usuario)

    @staticmethod
    def validar_registro(datos):
        es_valido = True
        if len(datos.get('nombre', '').strip()) < 2:
            flash('El nombre debe tener al menos 2 caracteres', 'error_nombre_registro')
            es_valido = False
        if len(datos.get('apellido', '').strip()) < 2:
            flash('El apellido debe tener al menos 2 caracteres', 'error_apellido_registro')
            es_valido = False
        if not EXPRESION_REGULAR_EMAIL.match(datos.get('correo', '').strip()):
            flash('Debe ingresar un formato de correo electrónico válido', 'error_correo_registro')
            es_valido = False
        else:
            usuario_existente = Usuario.obtener_por_correo({'correo': datos.get('correo').strip()})
            if usuario_existente:
                flash('El correo electrónico ya está registrado', 'error_correo_registro')
                es_valido = False
        if len(datos.get('contrasena', '')) < 8:
            flash('La contraseña debe tener un mínimo de 8 caracteres', 'error_contrasena_registro')
            es_valido = False
        if datos.get('contrasena') != datos.get('confirmar_contrasena'):
            flash('Las contraseñas no coinciden', 'error_confirmar_contrasena_registro')
            es_valido = False
        return es_valido