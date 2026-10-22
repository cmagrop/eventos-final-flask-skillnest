from flask import render_template, request, redirect, url_for, session
from models.modelo_evento import Evento

def inicializar_rutas_evento(app):
    @app.route('/eventos')
    def panel_principal():
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        usuario_id = session['usuario_id']
        eventos = Evento.obtener_todos_con_anfitrion()
        ids_eventos_unidos = Evento.obtener_ids_eventos_unidos({'usuario_id': usuario_id})
        return render_template('dashboard.html', eventos=eventos, ids_eventos_unidos=ids_eventos_unidos)

    @app.route('/eventos/nuevo', methods=['GET', 'POST'])
    def nuevo_evento():
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        if request.method == 'GET':
            return render_template('new_event.html')
        
        datos = {
            'nombre_evento': request.form.get('nombre_evento', '').strip(),
            'ubicacion': request.form.get('ubicacion', '').strip(),
            'fecha_evento': request.form.get('fecha_evento', '').strip(),
            'detalles': request.form.get('detalles', '').strip(),
            'usuario_id': session['usuario_id']
        }
        if not Evento.validar_evento(datos):
            return render_template('new_event.html', **datos)
        
        Evento.guardar(datos)
        return redirect(url_for('panel_principal'))

    @app.route('/eventos/<int:evento_id>')
    def ver_evento(evento_id):
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        evento = Evento.obtener_por_id({'id': evento_id})
        if not evento:
            return redirect(url_for('panel_principal'))
        asistentes = Evento.obtener_asistentes({'evento_id': evento_id})
        return render_template('show_event.html', evento=evento, asistentes=asistentes)

    @app.route('/eventos/<int:evento_id>/editar', methods=['GET', 'POST'])
    def editar_evento(evento_id):
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        evento = Evento.obtener_por_id({'id': evento_id})
        if not evento or evento.usuario_id != session['usuario_id']:
            return redirect(url_for('panel_principal'))
        if request.method == 'GET':
            return render_template('edit_event.html', evento=evento)
        
        datos = {
            'id': evento_id,
            'nombre_evento': request.form.get('nombre_evento', '').strip(),
            'ubicacion': request.form.get('ubicacion', '').strip(),
            'fecha_evento': request.form.get('fecha_evento', '').strip(),
            'detalles': request.form.get('detalles', '').strip()
        }
        if not Evento.validar_evento(datos):
            return render_template('edit_event.html', evento=datos)
        
        Evento.actualizar(datos)
        return redirect(url_for('ver_evento', evento_id=evento_id))

    @app.route('/eventos/<int:evento_id>/eliminar', methods=['POST'])
    def eliminar_evento(evento_id):
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        evento = Evento.obtener_por_id({'id': evento_id})
        if evento and evento.usuario_id == session['usuario_id']:
            Evento.eliminar({'id': evento_id})
        return redirect(url_for('panel_principal'))

    @app.route('/eventos/<int:evento_id>/unirse')
    def unirse_evento(evento_id):
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        Evento.unirse({'usuario_id': session['usuario_id'], 'evento_id': evento_id})
        return redirect(url_for('panel_principal'))

    @app.route('/eventos/<int:evento_id>/abandonar')
    def abandonar_evento(evento_id):
        if 'usuario_id' not in session:
            return redirect(url_for('inicio'))
        Evento.abandonar({'usuario_id': session['usuario_id'], 'evento_id': evento_id})
        return redirect(url_for('panel_principal'))