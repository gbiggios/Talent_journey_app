from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import Taller, Sala, DOCENTE, EstudianteTaller
from app.extensions import db
from app.routes.admin.decorators import admin_required
from app.forms import TallerForm

talleres_bp = Blueprint('talleres_admin', __name__)

@talleres_bp.route('/', endpoint='talleres_admin_listar')
@login_required
@admin_required  # Aplica la protección de admin
def talleres():
    talleres = Taller.query.all()
    salas = Sala.query.all()
    docentes = DOCENTE.query.all()
    form = TallerForm()
    return render_template('admin/talleres.html', talleres=talleres, salas=salas, docentes=docentes, form=form)


@talleres_bp.route('/create', methods=['POST'], endpoint='talleres_admin_crear')
@login_required
@admin_required
def create_taller():
    form = TallerForm()
    form.id_sala.choices = [(sala.id_sala, sala.nombre_sala) for sala in Sala.query.all()]
    form.id_docente.choices = [(docente.id_docente, f"{docente.nombre} {docente.apellido_paterno}") for docente in DOCENTE.query.all()]
    
    if form.validate_on_submit():
        nuevo_taller = Taller(
            nombre=form.nombre.data,
            horario=form.horario.data,
            id_sala=form.id_sala.data,
            id_docente=form.id_docente.data
        )
        db.session.add(nuevo_taller)
        db.session.commit()
        flash('Taller creado exitosamente.', 'success')
        return redirect(url_for('admin.talleres_admin.talleres_admin_listar'))

    # Si el formulario no es válido, renderizar la misma página con errores
    talleres = Taller.query.all()
    return render_template('admin/talleres.html', talleres=talleres, form=form)

@talleres_bp.route('/<int:taller_id>/delete', methods=['POST'], endpoint='talleres_admin_eliminar')
@login_required
@admin_required
def delete_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    db.session.delete(taller)
    db.session.commit()
    flash('Taller eliminado exitosamente.', 'success')
    return redirect(url_for('admin.talleres_admin.talleres_admin_listar'))

@talleres_bp.route('/<int:taller_id>/edit', methods=['GET', 'POST'], endpoint='talleres_admin_editar')
@login_required
@admin_required
def update_taller(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    form = TallerForm(obj=taller)
    form.id_sala.choices = [(sala.id_sala, sala.nombre_sala) for sala in Sala.query.all()]
    form.id_docente.choices = [(docente.id_docente, f"{docente.nombre} {docente.apellido_paterno}") for docente in DOCENTE.query.all()]

    if form.validate_on_submit():
        form.populate_obj(taller)
        db.session.commit()
        flash('Taller actualizado exitosamente.', 'success')
        return redirect(url_for('admin.talleres_admin.talleres_admin_listar'))

    return render_template('admin/edit_taller.html', form=form)

@talleres_bp.route('/listado', methods=['GET'], endpoint='talleres_admin_listado')
@login_required
@admin_required
def listado_talleres():
    talleres = Taller.query.all()
    
    # Añadir el conteo de estudiantes inscritos para cada taller
    for taller in talleres:
        taller.numero_estudiantes = EstudianteTaller.query.filter_by(taller_id=taller.taller_id).count()

    return render_template('admin/listado_talleres.html', talleres=talleres)

@talleres_bp.route('/detalle', methods=['GET'], endpoint='detalle_taller')
@login_required
@admin_required
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
