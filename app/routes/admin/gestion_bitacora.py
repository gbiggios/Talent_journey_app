from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required

from app.routes.admin.decorators import admin_required
from ...models import Taller, Clase
from ...extensions import db

bitacoras_bp = Blueprint('bitacoras_admin', __name__)

@bitacoras_bp.route('/taller_bitacoras', endpoint='bitacoras_admin_taller_bitacoras')
@login_required
@admin_required
def taller_bitacoras():
    talleres = Taller.query.all()
    return render_template('taller_bitacoras.html', talleres=talleres)

@bitacoras_bp.route('/taller_bitacoras/<int:taller_id>', endpoint='bitacoras_admin_ver_bitacoras')
@login_required
@admin_required
def ver_bitacoras(taller_id):
    taller = Taller.query.get_or_404(taller_id)
    clases = Clase.query.filter_by(taller_id=taller_id).order_by(Clase.fecha).all()
    return render_template('ver_bitacoras.html', taller=taller, clases=clases)

@bitacoras_bp.route('/bitacora_clase/<int:clase_id>', endpoint='bitacoras_admin_ver_bitacora_clase')
@login_required
@admin_required
def ver_bitacora_clase(clase_id):
    clase = Clase.query.get_or_404(clase_id)
    return render_template('ver_bitacora_clase.html', clase=clase)
