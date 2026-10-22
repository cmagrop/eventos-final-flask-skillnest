from flask import Flask
from controllers.controlador_usuarios import inicializar_rutas_usuario
from controllers.controlador_eventos import inicializar_rutas_evento

# Especificamos 'views' como la carpeta de plantillas (templates)
app = Flask(__name__, template_folder='views')
app.secret_key = 'clave_secreta_para_sesiones'

# Inicializar controladores
inicializar_rutas_usuario(app)
inicializar_rutas_evento(app)

if __name__ == '__main__':
    app.run(debug=True)