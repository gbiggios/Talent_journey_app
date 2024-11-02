from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from ...models import Estudiantes, Clase, AsistenciaEstudiante, Taller, EstudianteTaller, db
from ...forms import AsistenciaEstudianteForm
import logging

historial_bp = Blueprint('historial_admin', __name__)

# Configurar logging para depuración
logging.basicConfig(level=logging.DEBUG)

@historial_bp.route('/')
@login_required
def seleccionar_taller():
    talleres = Taller.query.all()
    return render_template('admin/seleccionar_taller.html', talleres=talleres)

@historial_bp.route('/taller/<int:taller_id>', methods=['GET', 'POST'])
@login_required
def historial_asistencia(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    clases = Clase.query.filter_by(taller_id=taller_id).all()
    estudiantes = Estudiantes.query.join(EstudianteTaller).filter_by(taller_id=taller_id).all()

    # Cargar el formulario de Flask-WTF
    form = AsistenciaEstudianteForm()

    # Si el método es POST, actualizar la asistencia y justificación
    if request.method == 'POST':
        logging.debug("POST request received.")
        logging.debug(f"Datos del formulario recibidos: {request.form}")

        if form.validate_on_submit():
            logging.debug("Formulario validado, procesando actualización...")

            for clase in clases:
                for estudiante in estudiantes:
                    # Generar las claves únicas para identificar cada entrada
                    presencia_key = f'asistencia_{estudiante.id_estudiante}_{clase.id_clase}'
                    justificacion_key = f'justificacion_{estudiante.id_estudiante}_{clase.id_clase}'

                    # Obtener los valores del formulario
                    presencia = request.form.get(presencia_key) == 'on'
                    justificacion = request.form.get(justificacion_key)

                    logging.debug(f"Procesando estudiante {estudiante.nombre} en clase {clase.fecha}")
                    logging.debug(f"Presencia: {presencia}, Justificación: {justificacion}")

                    # Buscar la asistencia o crear una nueva
                    asistencia = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase, id_estudiante=estudiante.id_estudiante).first()
                    if asistencia:
                        logging.debug("Asistencia encontrada, actualizando...")
                        asistencia.presencia = presencia
                        asistencia.justificacion = justificacion if not presencia else None
                    else:
                        logging.debug("No se encontró asistencia, creando una nueva...")
                        nueva_asistencia = AsistenciaEstudiante(
                            id_clase=clase.id_clase,
                            id_estudiante=estudiante.id_estudiante,
                            presencia=presencia,
                            justificacion=justificacion if not presencia else None
                        )
                        db.session.add(nueva_asistencia)

            try:
                logging.debug("Intentando guardar en la base de datos...")
                db.session.commit()
                flash('Asistencia actualizada correctamente.')
            except Exception as e:
                db.session.rollback()  # Si hay error, hacemos rollback
                logging.error(f"Error al guardar en la base de datos: {e}")
                flash('Ocurrió un error al intentar actualizar la asistencia.', 'error')

            return redirect(url_for('historial_admin.historial_asistencia', taller_id=taller_id))
        else:
            logging.debug("El formulario no se validó correctamente.")

    # Si el método es GET, generar los diccionarios para mostrar los datos
    asistencia_dict = {}
    justificacion_dict = {}
    porcentaje_asistencia = {}
    
    for estudiante in estudiantes:
        total_clases = len(clases)
        clases_asistidas = 0
        
        for clase in clases:
            asistencia = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase, id_estudiante=estudiante.id_estudiante).first()
            if estudiante.id_estudiante not in asistencia_dict:
                asistencia_dict[estudiante.id_estudiante] = {}
                justificacion_dict[estudiante.id_estudiante] = {}

            asistencia_dict[estudiante.id_estudiante][clase.id_clase] = asistencia.presencia if asistencia else False
            justificacion_dict[estudiante.id_estudiante][clase.id_clase] = asistencia.justificacion if asistencia else ""

            # Contar clases asistidas para calcular el porcentaje
            if asistencia and asistencia.presencia:
                clases_asistidas += 1

        # Calcular el porcentaje de asistencia
        porcentaje_asistencia[estudiante.id_estudiante] = (clases_asistidas / total_clases) * 100 if total_clases > 0 else 0

    return render_template('admin/historial_asistencia.html', form=form, taller=taller, clases=clases, estudiantes=estudiantes, asistencia_dict=asistencia_dict, justificacion_dict=justificacion_dict, porcentaje_asistencia=porcentaje_asistencia)
