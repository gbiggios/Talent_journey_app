from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

from app.routes.admin.decorators import admin_required
from ...models import Estudiantes
from ...extensions import db
from ...forms import EstudiantesForm
from ...utils import allowed_file, cargar_datos_excel

estudiantes_bp = Blueprint('estudiantes_admin', __name__)

@estudiantes_bp.route('/', endpoint='estudiantes_admin_home')
@login_required
@admin_required
def estudiantes():
    estudiantes = Estudiantes.query.all()
    form = EstudiantesForm()
    return render_template('admin/estudiantes.html', estudiantes=estudiantes, form=form)

@estudiantes_bp.route('/create', methods=['POST'], endpoint='estudiantes_admin_create')
@login_required
@admin_required
def create_estudiante():
    form = EstudiantesForm()
    if form.validate_on_submit():
        nuevo_estudiante = Estudiantes(
            rut_estudiante=form.rut_estudiante.data,
            nombre=form.nombre.data,
            apellido_paterno=form.apellido_paterno.data,
            apellido_materno=form.apellido_materno.data,
            curso=form.curso.data,
            correo_institucional=form.correo_institucional.data
        )
        
        db.session.add(nuevo_estudiante)
        db.session.commit()
        flash('Estudiante creado exitosamente.', 'success')
        return redirect(url_for('admin.estudiantes_admin.estudiantes_admin_home'))
    
    return render_template('admin/estudiantes.html', form=form)

@estudiantes_bp.route('/<int:id_estudiante>/delete', methods=['POST'], endpoint='estudiantes_admin_delete')
@login_required
@admin_required
def delete_estudiante(id_estudiante):
    estudiante = Estudiantes.query.get_or_404(id_estudiante)
    db.session.delete(estudiante)
    db.session.commit()
    flash('Estudiante eliminado exitosamente.', 'success')
    return redirect(url_for('admin.estudiantes_admin.estudiantes_admin_home'))

@estudiantes_bp.route('/<int:id_estudiante>/edit', methods=['POST'], endpoint='estudiantes_admin_update')
@login_required
@admin_required
def update_estudiante(id_estudiante):
    estudiante = Estudiantes.query.get_or_404(id_estudiante)
    form = EstudiantesForm(obj=estudiante)
    if form.validate_on_submit():
        form.populate_obj(estudiante)
        db.session.commit()
        flash('Estudiante actualizado exitosamente.', 'success')
        return redirect(url_for('estudiantes_admin.estudiantes_admin_home'))
    
    return render_template('admin/estudiantes.html', estudiante=estudiante, form=form)


@estudiantes_bp.route('/cargar_estudiantes', methods=['GET', 'POST'], endpoint='estudiantes_admin_cargar')
@login_required
@admin_required
def cargar_estudiantes():
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se ha seleccionado ningún archivo')
            return redirect(request.url)
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            flash('No se ha seleccionado ningún archivo')
            return redirect(request.url)

        if archivo and allowed_file(archivo.filename):
            filename = secure_filename(archivo.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            archivo.save(filepath)
            cargar_datos_excel(filepath)
            flash('Los estudiantes se han cargado exitosamente')
            return redirect(url_for('admin.estudiantes_admin.estudiantes_admin_home'))
    
    return render_template('admin/cargar_estudiantes.html')
