from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required
from app.models import Estudiantes, Taller, EstudianteTaller
from app.extensions import db
from app.routes.admin.decorators import admin_required
from app.forms import EstudianteTallerForm

# Crear el Blueprint
estudiantes_taller_bp = Blueprint('estudiantes_taller_admin', __name__)

# Rutas

@estudiantes_taller_bp.route('/', methods=['GET', 'POST'], endpoint='estudiantes_taller_admin_gestionar')
@login_required
@admin_required
def gestionar_estudiantes_taller():
    form = EstudianteTallerForm()

    if form.validate_on_submit():
        taller_id = form.taller_id.data
        id_estudiantes = request.form.getlist('id_estudiantes')  # Obtener todos los estudiantes seleccionados

        for id_estudiante in id_estudiantes:
            # Verificar si ya existe la asignación
            asignacion_existente = EstudianteTaller.query.filter_by(
                id_estudiante=id_estudiante,
                taller_id=taller_id
            ).first()

            if not asignacion_existente:
                nueva_asignacion = EstudianteTaller(
                    id_estudiante=id_estudiante,
                    taller_id=taller_id
                )
                db.session.add(nueva_asignacion)

        db.session.commit()
        flash('Estudiantes asignados correctamente al taller', 'success')
        return redirect(url_for('admin.estudiantes_taller_admin.estudiantes_taller_admin_gestionar'))

    estudiantes = Estudiantes.query.all()
    talleres = Taller.query.all()

    return render_template('admin/estudiantes_taller.html', estudiantes=estudiantes, talleres=talleres, form=form)

@estudiantes_taller_bp.route('/delete/<int:id_taller_estudiante>', methods=['POST'], endpoint='estudiantes_taller_admin_delete')
@login_required
@admin_required
def delete_estudiante_taller(id_taller_estudiante):
    asignacion = EstudianteTaller.query.get_or_404(id_taller_estudiante)
    db.session.delete(asignacion)
    db.session.commit()
    flash('Asignación eliminada correctamente', 'success')
    return redirect(url_for('admin.estudiantes_taller_admin.estudiantes_taller_admin_gestionar'))

@estudiantes_taller_bp.route('/load_students/<int:taller_id>', methods=['GET'], endpoint='load_students')
@login_required
@admin_required
def load_students(taller_id):
    # Obtener los estudiantes asignados a este taller
    asignaciones = EstudianteTaller.query.filter_by(taller_id=taller_id).limit(10).all()
    return render_template('admin/estudiantes_list.html', asignaciones=asignaciones)
