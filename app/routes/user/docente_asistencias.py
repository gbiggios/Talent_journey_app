from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ...models import Clase, EstudianteTaller, AsistenciaEstudiante
from ...extensions import db

docente_asistencias_bp = Blueprint('docente_asistencias', __name__)

@docente_asistencias_bp.route('/<int:clase_id>', methods=['GET', 'POST'])
@login_required
def pasar_asistencia(clase_id):
    clase = Clase.query.get_or_404(clase_id)

    # Verificar que el docente esté asignado a la clase/taller
    if clase.taller.id_docente != current_user.id_docente:
        flash('No tienes permisos para pasar asistencia en esta clase.', 'danger')
        return redirect(url_for('docente.dashboard'))

    estudiantes_taller = EstudianteTaller.query.filter_by(taller_id=clase.taller_id).all()
    estudiantes = [et.estudiante for et in estudiantes_taller]

    if request.method == 'POST':
        for estudiante in estudiantes:
            presencia = f'presencia_{estudiante.id_estudiante}' in request.form
            justificacion = request.form.get(f'justificacion_{estudiante.id_estudiante}', '')

            asistencia = AsistenciaEstudiante.query.filter_by(id_clase=clase_id, id_estudiante=estudiante.id_estudiante).first()
            if asistencia:
                asistencia.presencia = presencia
                asistencia.justificacion = justificacion
            else:
                nueva_asistencia = AsistenciaEstudiante(
                    id_clase=clase_id,
                    id_estudiante=estudiante.id_estudiante,
                    presencia=presencia,
                    justificacion=justificacion
                )
                db.session.add(nueva_asistencia)
        
        db.session.commit()
        flash('Asistencia actualizada exitosamente.', 'success')
        return redirect(url_for('docente.dashboard'))

    asistencias = {a.id_estudiante: a for a in AsistenciaEstudiante.query.filter_by(id_clase=clase_id).all()}
    return render_template('docente/pasar_asistencia.html', clase=clase, estudiantes=estudiantes, asistencias=asistencias)
