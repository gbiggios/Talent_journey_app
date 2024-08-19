from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import Sala
from app.extensions import db
from app.forms import SalaForm

salas_bp = Blueprint('salas_admin', __name__)

@salas_bp.route('/', endpoint='salas_admin_listar')
@login_required
def salas():
    form = SalaForm()
    salas = Sala.query.all()
    return render_template('admin/salas.html', salas=salas, form=form)

@salas_bp.route('/create', methods=['GET', 'POST'], endpoint='salas_admin_crear')
@login_required
def create_sala():
    form = SalaForm()
    if form.validate_on_submit():
        nombre_sala = form.nombre_sala.data
        nueva_sala = Sala(nombre_sala=nombre_sala)
        db.session.add(nueva_sala)
        db.session.commit()
        flash('Sala creada exitosamente.', 'success')
        return redirect(url_for('admin.salas_admin.salas_admin_listar'))
    return render_template('admin/salas.html', salas=Sala.query.all(), form=form)

@salas_bp.route('/<int:id_sala>/delete', methods=['POST'], endpoint='salas_admin_eliminar')
@login_required
def delete_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    db.session.delete(sala)
    db.session.commit()
    flash('Sala eliminada exitosamente.', 'success')
    return redirect(url_for('admin.salas_admin.salas_admin_listar'))

@salas_bp.route('/<int:id_sala>/edit', methods=['GET', 'POST'], endpoint='salas_admin_editar')
@login_required
def update_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    form = SalaForm(obj=sala)
    
    if form.validate_on_submit():
        sala.nombre_sala = form.nombre_sala.data
        db.session.commit()
        flash('Sala actualizada exitosamente.', 'success')
        return redirect(url_for('admin.salas_admin.salas_admin_listar'))
    
    return render_template('admin/salas.html', salas=Sala.query.all(), form=form)
