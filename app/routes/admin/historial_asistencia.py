from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from ...models import Estudiantes, Clase, AsistenciaEstudiante, Taller, EstudianteTaller

historial_bp = Blueprint('historial_admin', __name__)

@historial_bp.route('/')
@login_required
def seleccionar_taller():
    talleres = Taller.query.all()
    return render_template('admin/seleccionar_taller.html', talleres=talleres)

@historial_bp.route('/taller/<int:taller_id>')
@login_required
def historial_asistencia(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    clases = Clase.query.filter_by(taller_id=taller_id).all()
    estudiantes = Estudiantes.query.join(EstudianteTaller).filter_by(taller_id=taller_id).all()
    
    # Obtener las asistencias de todas las clases para cada estudiante
    asistencia_dict = {}
    for clase in clases:
        for estudiante in estudiantes:
            asistencia = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase, id_estudiante=estudiante.id_estudiante).first()
            if estudiante.id_estudiante not in asistencia_dict:
                asistencia_dict[estudiante.id_estudiante] = {}
            asistencia_dict[estudiante.id_estudiante][clase.id_clase] = asistencia.presencia if asistencia else False

    return render_template('admin/historial_asistencia.html', taller=taller, clases=clases, estudiantes=estudiantes, asistencia_dict=asistencia_dict)
