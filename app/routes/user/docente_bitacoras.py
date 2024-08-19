from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ...models import Clase, Taller
from ...extensions import db

bitacoras_bp = Blueprint('docente_bitacoras', __name__)

@bitacoras_bp.route('/')
@login_required
def ver_bitacoras():
    talleres = Taller.query.filter_by(id_docente=current_user.id_docente).all()
    return render_template('bitacoras/ver_bitacoras.html', talleres=talleres)

@bitacoras_bp.route('/<int:clase_id>', methods=['GET', 'POST'])
@login_required
def completar_bitacora(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    
    # Verificar que el docente esté asignado a la clase/taller
    if clase.taller.id_docente != current_user.id_docente:
        flash('No tienes permisos para completar la bitácora de esta clase.', 'danger')
        return redirect(url_for('docente_bitacoras.ver_bitacoras'))

    if request.method == 'POST':
        clase.comentario_bitacora = request.form['comentario_bitacora']
        db.session.commit()
        flash('Bitácora completada correctamente.', 'success')
        return redirect(url_for('docente_bitacoras.ver_bitacoras'))

    return render_template('bitacoras/completar_bitacora.html', clase=clase)
