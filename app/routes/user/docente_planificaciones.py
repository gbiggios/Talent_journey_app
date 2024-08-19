from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Planificacion, Taller
from app.extensions import db

# Crear el Blueprint para las rutas de Planificación de docentes
planificacion_bp = Blueprint('planificacion_docente', __name__)

# Ruta para listar las planificaciones del docente
@planificacion_bp.route('/')
@login_required
def listar_planificaciones_docente():
    talleres = Taller.query.filter_by(id_docente=current_user.id_docente).all()
    planificaciones = Planificacion.query.filter(Planificacion.taller_id.in_([t.taller_id for t in talleres])).all()

    # Preparar datos para el template
    estados = {}
    meses = ['Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre']

    for mes in meses:
        planificacion_mes = next((p for p in planificaciones if p.mes == mes), None)
        if planificacion_mes:
            if all([planificacion_mes.habilidades, planificacion_mes.recursos, planificacion_mes.actividades]):
                estados[mes] = 'Planificada'
            else:
                estados[mes] = 'En proceso'
        else:
            estados[mes] = 'No realizado'

    return render_template('user/docente_planificaciones.html', 
                           talleres=talleres, 
                           planificaciones=planificaciones, 
                           estados=estados, 
                           meses=meses)

# Ruta para que el docente pueda definir el objetivo general del taller
@planificacion_bp.route('/talleres/<int:id>/editar_objetivo', methods=['GET', 'POST'])
@login_required
def editar_objetivo_taller_docente(id):
    taller = Taller.query.filter_by(taller_id=id, id_docente=current_user.id_docente).first_or_404()

    if request.method == 'POST':
        taller.objetivo_general = request.form.get('objetivo_general', '')  # Asegúrate de manejar el caso en que no se proporcione un objetivo
        db.session.commit()
        flash('Objetivo general actualizado exitosamente')
        return redirect(url_for('planificacion_docente.listar_planificaciones_docente'))

    return render_template('user/docente_planificaciones.html', taller=taller)

# Ruta para crear una nueva planificación desde la perspectiva del docente
@planificacion_bp.route('/<int:taller_id>/nueva', methods=['GET', 'POST'])
@login_required
def planificacion_taller_docente(taller_id):
    taller = Taller.query.filter_by(id_docente=current_user.id_docente, taller_id=taller_id).first_or_404()

    if request.method == 'POST':
        mes = request.form.get('mes')
        habilidades = request.form.get('habilidades')
        recursos = request.form.get('recursos')
        actividades = request.form.get('actividades')
        estado = request.form.get('estado', 'No realizado')  # Default value

        nueva_planificacion = Planificacion(
            taller_id=taller_id,
            mes=mes,
            habilidades=habilidades,
            recursos=recursos,
            actividades=actividades,
            estado=estado
        )
        
        db.session.add(nueva_planificacion)
        db.session.commit()

        flash('Planificación creada exitosamente')
        return redirect(url_for('planificacion_docente.listar_planificaciones_docente'))

    return render_template('user/docente_planificaciones.html', taller=taller)

# Ruta para editar una planificación existente desde la perspectiva del docente
@planificacion_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_planificacion_docente(id):
    planificacion = Planificacion.query.filter_by(id_planificacion=id).first_or_404()

    if request.method == 'POST':
        planificacion.mes = request.form.get('mes')
        planificacion.habilidades = request.form.get('habilidades')
        planificacion.recursos = request.form.get('recursos')
        planificacion.actividades = request.form.get('actividades')
        planificacion.estado = request.form.get('estado')

        db.session.commit()

        flash('Planificación actualizada exitosamente')
        return redirect(url_for('planificacion_docente.listar_planificaciones_docente'))

    return render_template('user/docente_planificaciones.html', planificacion=planificacion)
