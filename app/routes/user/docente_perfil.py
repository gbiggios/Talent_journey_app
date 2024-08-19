from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from ...extensions import db

perfil_bp = Blueprint('docente_perfil', __name__)

@perfil_bp.route('/')
@login_required
def ver_perfil():
    return render_template('perfil/ver_perfil.html', user=current_user)

@perfil_bp.route('/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        current_user.username = request.form['username']

        # Validar si se quiere cambiar la contraseña
        if request.form['password']:
            current_user.set_password(request.form['password'])

        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('docente_perfil.ver_perfil'))
    
    return render_template('perfil/editar_perfil.html', user=current_user)
