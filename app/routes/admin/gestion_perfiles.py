from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from ...models import User, DOCENTE
from ...extensions import db

gestion_perfiles_bp = Blueprint('perfiles_admin', __name__)

@gestion_perfiles_bp.route('/', endpoint='perfiles_admin_listar')
@login_required
def listar_perfiles():
    if not current_user.is_admin:
        flash('No tiene permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente_perfil.ver_perfil'))

    usuarios = User.query.all()
    return render_template('admin/perfiles.html', usuarios=usuarios)

@gestion_perfiles_bp.route('/editar/<int:user_id>', methods=['GET', 'POST'], endpoint='perfiles_admin_editar')
@login_required
def editar_perfil(user_id):
    if not current_user.is_admin:
        flash('No tiene permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente_perfil.ver_perfil'))

    usuario = User.query.get_or_404(user_id)
    if request.method == 'POST':
        usuario.username = request.form['username']
        if request.form['password']:
            usuario.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        db.session.commit()
        flash('Perfil actualizado exitosamente.', 'success')
        return redirect(url_for('perfiles_admin_listar'))

    return render_template('perfiles/editar_perfil.html', usuario=usuario)

@gestion_perfiles_bp.route('/eliminar/<int:user_id>', methods=['POST'], endpoint='perfiles_admin_eliminar')
@login_required
def eliminar_perfil(user_id):
    if not current_user.is_admin:
        flash('No tiene permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente_perfil.ver_perfil'))

    usuario = User.query.get_or_404(user_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Perfil eliminado correctamente.', 'success')
    return redirect(url_for('perfiles_admin_listar'))

@gestion_perfiles_bp.route('/crear', methods=['GET', 'POST'], endpoint='perfiles_admin_crear')
@login_required
def crear_perfil():
    if not current_user.is_admin:
        flash('No tiene permisos para acceder a esta página.', 'danger')
        return redirect(url_for('docente_perfil.ver_perfil'))

    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        is_admin = 'is_admin' in request.form

        nuevo_usuario = User(username=username, password=password, is_admin=is_admin)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Perfil creado exitosamente.', 'success')
        return redirect(url_for('perfiles_admin_listar'))

    return render_template('perfiles/crear_perfil.html')
