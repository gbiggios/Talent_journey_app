from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ...models import Taller
from ...extensions import db

objetivo_bp = Blueprint('docente_objetivos', __name__)

@objetivo_bp.route('/taller/<int:taller_id>', methods=['GET', 'POST'])
@login_required
def definir_objetivo(taller_id):
    # Verificar que el docente está asignado al taller antes de permitirle definir el objetivo
    taller = Taller.query.filter_by(taller_id=taller_id, id_docente=current_user.id_docente).first_or_404()

    if request.method == 'POST':
        taller.objetivo_general = request.form['objetivo_general']
        db.session.commit()
        flash('Objetivo del taller actualizado correctamente.', 'success')
        return redirect(url_for('docente_objetivos.definir_objetivo', taller_id=taller_id))

    return render_template('talleres/definir_objetivo.html', taller=taller)
