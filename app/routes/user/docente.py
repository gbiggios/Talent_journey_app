from datetime import date
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from ...models import DOCENTE, Taller, Clase, AsistenciaEstudiante
from ...extensions import db

docente_bp = Blueprint('docente', __name__)

@docente_bp.route('/dashboard')
@login_required
def dashboard():
    # Verificar si el usuario actual es un docente o un administrador
    if not current_user.is_docente and not current_user.is_admin:
        abort(403)  # Denegar acceso si no es docente ni administrador

    # Obtener los talleres asignados al docente
    talleres = Taller.query.filter_by(id_docente=current_user.id_docente).all()
    #Fecha actual
    current_date = date.today()
    return render_template('user/docente_dashboard.html', talleres=talleres,current_date=current_date)

@docente_bp.route('/clase/<int:clase_id>', methods=['GET', 'POST'])
@login_required
def clase_detalle(clase_id):
    # Obtener la clase correspondiente
    clase = Clase.query.get_or_404(clase_id)

    if request.method == 'POST':
        # Procesar asistencia de estudiantes
        procesar_asistencia(clase, request.form)
        
        # Actualizar comentario de bitácora
        clase.comentario_bitacora = request.form.get('comentario_bitacora', '')
        db.session.commit()

        flash('Asistencia y bitácora actualizadas correctamente.')
        return redirect(url_for('docente.dashboard'))  # Correcta referencia al endpoint
    
    # Obtener asistencias existentes
    asistencias = {a.id_estudiante: a for a in AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase).all()}
    return render_template('user/clase_detalle.html', clase=clase, asistencias=asistencias)

def procesar_asistencia(clase, form_data):
    """Función para procesar y actualizar la asistencia de los estudiantes"""
    for estudiante in clase.taller.estudiantes_taller:
        presencia = form_data.get(f'presencia_{estudiante.id_estudiante}') == 'on'
        justificacion = form_data.get(f'justificacion_{estudiante.id_estudiante}', '')

        asistencia = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase, id_estudiante=estudiante.id_estudiante).first()
        if asistencia:
            asistencia.presencia = presencia
            asistencia.justificacion = justificacion
        else:
            nueva_asistencia = AsistenciaEstudiante(
                id_clase=clase.id_clase,
                id_estudiante=estudiante.id_estudiante,
                presencia=presencia,
                justificacion=justificacion
            )
            db.session.add(nueva_asistencia)
