from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required
from app.models import Taller, Sala, DOCENTE, EstudianteTaller
from app.extensions import db
from app.routes.admin.decorators import admin_required  # Asegúrate de que esto esté bien importado

talleres_bp = Blueprint('talleres_admin', __name__)

@talleres_bp.route('/', endpoint='talleres_admin_listar')
@login_required
@admin_required  # Aplica la protección de admin
def talleres():
    talleres = Taller.query.all()
    salas = Sala.query.all()
    docentes = DOCENTE.query.all()
    return render_template('admin/talleres.html', talleres=talleres, salas=salas, docentes=docentes)

@talleres_bp.route('/create', methods=['POST'], endpoint='talleres_admin_crear')
@login_required
@admin_required  # Aplica la protección de admin
def create_taller():
    nombre = request.form['nombre']
    horario = request.form['horario']
    id_sala = request.form['id_sala']
    id_docente = request.form['id_docente']
    
    nuevo_taller = Taller(
        nombre=nombre,
        horario=horario,
        id_sala=id_sala,
        id_docente=id_docente
    )
    
    db.session.add(nuevo_taller)
    db.session.commit()
    return redirect(url_for('talleres_admin.talleres_admin_listar'))

@talleres_bp.route('/<int:taller_id>/delete', methods=['POST'], endpoint='talleres_admin_eliminar')
@login_required
@admin_required  # Aplica la protección de admin
def delete_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    db.session.delete(taller)
    db.session.commit()
    return redirect(url_for('talleres_admin.talleres_admin_listar'))

@talleres_bp.route('/<int:taller_id>/edit', methods=['GET'], endpoint='talleres_admin_editar_get')
@login_required
@admin_required  # Aplica la protección de admin
def edit_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    salas = Sala.query.all()
    docentes = DOCENTE.query.all()
    return render_template('admin/edit_taller.html', taller=taller, salas=salas, docentes=docentes)

@talleres_bp.route('/<int:taller_id>/edit', methods=['POST'], endpoint='talleres_admin_editar_post')
@login_required
@admin_required  # Aplica la protección de admin
def update_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    taller.nombre = request.form['nombre']
    taller.horario = request.form['horario']
    taller.id_sala = request.form['id_sala']
    taller.id_docente = request.form['id_docente']
    
    db.session.commit()
    return redirect(url_for('talleres_admin.talleres_admin_listar'))

@talleres_bp.route('/listado', methods=['GET'], endpoint='talleres_admin_listado')
@login_required
@admin_required  # Aplica la protección de admin
def listado_talleres():
    talleres = Taller.query.all()
    
    # Añadir el conteo de estudiantes inscritos para cada taller
    for taller in talleres:
        taller.numero_estudiantes = EstudianteTaller.query.filter_by(taller_id=taller.taller_id).count()

    return render_template('admin/listado_talleres.html', talleres=talleres)

@talleres_bp.route('/detalle', methods=['GET'], endpoint='detalle_taller')
@login_required
@admin_required  # Aplica la protección de admin
def detalle_taller():
    taller_id = request.args.get('taller_id')
    asignaciones = EstudianteTaller.query.filter_by(taller_id=taller_id).all()
    estudiantes = []

    for asignacion in asignaciones:
        estudiante = {
            'nombre': asignacion.estudiante.nombre + ' ' + asignacion.estudiante.apellido_paterno,
            'rut_estudiante': asignacion.estudiante.rut_estudiante,
            'curso': asignacion.estudiante.curso
        }
        estudiantes.append(estudiante)

    return jsonify(estudiantes=estudiantes)
