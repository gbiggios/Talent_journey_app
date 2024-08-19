from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Estudiantes, Taller, EstudianteTaller
from app.extensions import db
from app.routes.admin.decorators import admin_required

# Crear el Blueprint
estudiantes_taller_bp = Blueprint('estudiantes_taller_admin', __name__)

@estudiantes_taller_bp.route('/', methods=['GET', 'POST'], endpoint='estudiantes_taller_admin_gestionar')
@login_required
@admin_required  # Aplica la protección de admin
def gestionar_estudiantes_taller():
    if request.method == 'POST':
        taller_id = request.form['taller_id']
        id_estudiantes = request.form.getlist('id_estudiantes')
        
        for id_estudiante in id_estudiantes:
            nueva_asignacion = EstudianteTaller(
                id_estudiante=id_estudiante,
                taller_id=taller_id
            )
            db.session.add(nueva_asignacion)
        
        db.session.commit()
        flash('Estudiantes asignados correctamente al taller', 'success')
        return redirect(url_for('estudiantes_taller_admin_gestionar'))
    
    estudiantes = Estudiantes.query.all()
    talleres = Taller.query.all()
    cursos = list(set(estudiante.curso for estudiante in estudiantes))
    asignaciones = EstudianteTaller.query.all()

    return render_template('admin/estudiantes_taller.html', estudiantes=estudiantes, talleres=talleres, cursos=cursos, asignaciones=asignaciones)

@estudiantes_taller_bp.route('/delete/<int:id_taller_estudiante>', methods=['POST'], endpoint='estudiantes_taller_admin_delete')
@login_required
@admin_required  # Aplica la protección de admin
def delete_estudiante_taller(id_taller_estudiante):
    asignacion = EstudianteTaller.query.get_or_404(id_taller_estudiante)
    db.session.delete(asignacion)
    db.session.commit()
    flash('Asignación eliminada correctamente', 'success')
    return redirect(url_for('estudiantes_taller_admin_gestionar'))
