from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from models.modelo_usuario import Usuario

def inicializar_rutas_usuario(app):
    bcrypt = Bcrypt(app)

    @app.route('/')
    def inicio():
        if 'usuario_id' in session:
            return redirect(url_for('panel_principal'))
        return render_template('index.html')

    @app.route('/registro', methods=['POST'])
    def registrar():
        datos = {
            'nombre': request.form.get('nombre', ''),
            'apellido': request.form.get('apellido', ''),
            'correo': request.form.get('correo', ''),
            'contrasena': request.form.get('contrasena', ''),
            'confirmar_contrasena': request.form.get('confirmar_contrasena', '')
        }
        if not Usuario.validar_registro(datos):
            return redirect(url_for('inicio'))
        
        hash_contrasena = bcrypt.generate_password_hash(datos['contrasena']).decode('utf-8')
        datos['contrasena'] = hash_contrasena
        usuario_id = Usuario.guardar(datos)
        
        session['usuario_id'] = usuario_id
        session['nombre'] = datos['nombre']
        return redirect(url_for('panel_principal'))

    @app.route('/login', methods=['POST'])
    def iniciar_sesion():
        correo = request.form.get('correo', '').strip()
        contrasena = request.form.get('contrasena', '')
        usuario = Usuario.obtener_por_correo({'correo': correo})
        
        if not usuario or not bcrypt.check_password_hash(usuario.contrasena, contrasena):
            flash('Credenciales inválidas', 'error_login')
            return redirect(url_for('inicio'))
        
        session['usuario_id'] = usuario.id
        session['nombre'] = usuario.nombre
        return redirect(url_for('panel_principal'))

    @app.route('/logout')
    def cerrar_sesion():
        session.clear()
        return redirect(url_for('inicio'))