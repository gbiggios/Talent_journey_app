from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...extensions import db
from ...models import Planificacion, Taller
from flask_login import current_user, login_required
from app.routes.admin.decorators import admin_required
from app.forms import PlanificacionForm

# Crear el Blueprint para las rutas de Planificación
planificacion_bp = Blueprint('planificacion_admin', __name__)

# Ruta para listar todas las planificaciones (solo admin)
@planificacion_bp.route('/', methods=['GET'], endpoint='listar_planificaciones_admin')
@login_required
@admin_required
def listar_planificaciones_admin():
    talleres = Taller.query.all()
    form= PlanificacionForm()

    if not talleres:
        flash('No hay talleres disponibles.')
        return redirect(url_for('admin.dashboard'))  # Redirige a un lugar seguro si no hay talleres

    # Seleccionar el primer taller como predeterminado
    taller_seleccionado = talleres[0]
    planificaciones = {
        planificacion.mes: planificacion for planificacion in Planificacion.query.filter_by(taller_id=taller_seleccionado.taller_id).all()
    }

    meses = ["marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    siguiente_mes = None
    puede_crear = True

    for i, mes in enumerate(meses):
        if mes not in planificaciones:
            siguiente_mes = mes
            if i > 0 and meses[i - 1] not in planificaciones:
                puede_crear = False
            break

    return render_template(
        'admin/gestionar_planificaciones.html',
        talleres=talleres,
        taller_seleccionado=taller_seleccionado,
        planificaciones=planificaciones,
        siguiente_mes=siguiente_mes,
        puede_crear=puede_crear,
        form=form
    )

# Ruta para seleccionar un taller específico
@planificacion_bp.route('/<int:taller_id>', methods=['GET'], endpoint='listar_planificaciones_taller')
@login_required
@admin_required
def listar_planificaciones_taller(taller_id):
    taller_seleccionado = Taller.query.get_or_404(taller_id)
    talleres = Taller.query.all()
    form= PlanificacionForm()
    planificaciones = {
        planificacion.mes: planificacion for planificacion in Planificacion.query.filter_by(taller_id=taller_seleccionado.taller_id).all()
    }

    meses = ["marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    siguiente_mes = None
    puede_crear = True

    for i, mes in enumerate(meses):
        if mes not in planificaciones:
            siguiente_mes = mes
            if i > 0 and meses[i - 1] not in planificaciones:
                puede_crear = False
            break

    return render_template(
        'admin/gestionar_planificaciones.html',
        talleres=talleres,
        taller_seleccionado=taller_seleccionado,
        planificaciones=planificaciones,
        siguiente_mes=siguiente_mes,
        puede_crear=puede_crear, form=form
    )

# Ruta para crear una nueva planificación (solo admin)
@planificacion_bp.route('/nueva', methods=['POST'], endpoint='crear_planificacion_admin')
@login_required
@admin_required
def crear_planificacion_admin():
    taller_id = request.form['taller_id']
    form= PlanificacionForm()
    
    # Validar que se haya seleccionado un taller válido
    if not taller_id or not taller_id.isdigit() or not Taller.query.get(taller_id):
        flash('Por favor, selecciona un taller válido.')
        return redirect(url_for('admin.planificacion_admin.listar_planificaciones_admin'))

    nueva_planificacion = Planificacion(
        taller_id=taller_id,
        mes=request.form['mes'],
        habilidades=','.join(request.form['habilidades'].split(',')),  # Convertir lista a cadena
        recursos=','.join(request.form['recursos'].split(',')),  # Convertir lista a cadena
        actividades=','.join(request.form['actividades'].split(',')),  # Convertir lista a cadena
        estado=request.form['estado']
    )
    db.session.add(nueva_planificacion)
    db.session.commit()
    flash('Planificación creada exitosamente')

    return redirect(url_for('admin.planificacion_admin.listar_planificaciones_taller', taller_id=taller_id,form=form))

# Ruta para editar una planificación existente (solo admin)
@planificacion_bp.route('/editar', methods=['POST'], endpoint='editar_planificacion_admin')
@login_required
@admin_required
def editar_planificacion_admin():
    planificacion = Planificacion.query.get_or_404(request.form['id'])

    form= PlanificacionForm()

    taller_id = request.form['taller_id']
    
    # Validar que se haya seleccionado un taller válido
    if not taller_id or not taller_id.isdigit() or not Taller.query.get(taller_id):
        flash('Por favor, selecciona un taller válido.')
        return redirect(url_for('admin.planificacion_admin.listar_planificaciones_taller', taller_id=planificacion.taller_id))

    planificacion.taller_id = taller_id
    planificacion.mes = request.form['mes']
    planificacion.habilidades = ','.join(request.form['habilidades'].split(','))  # Convertir lista a cadena
    planificacion.recursos = ','.join(request.form['recursos'].split(','))  # Convertir lista a cadena
    planificacion.actividades = ','.join(request.form['actividades'].split(','))  # Convertir lista a cadena
    planificacion.estado = request.form['estado']
    db.session.commit()
    flash('Planificación actualizada exitosamente')

    return redirect(url_for('admin.planificacion_admin.listar_planificaciones_taller', taller_id=taller_id, form=form))

# Ruta para eliminar una planificación (solo admin)
@planificacion_bp.route('/eliminar', methods=['POST'], endpoint='eliminar_planificacion_admin')
@login_required
@admin_required
def eliminar_planificacion_admin():
    planificacion = Planificacion.query.get_or_404(request.form['id'])
    taller_id = planificacion.taller_id
    db.session.delete(planificacion)
    db.session.commit()
    flash('Planificación eliminada exitosamente')

    return redirect(url_for('admin.planificacion_admin.listar_planificaciones_taller', taller_id=taller_id))



# Ruta para actualizar el objetivo general de un taller (solo admin)
@planificacion_bp.route('/actualizar_objetivo_general', methods=['POST'], endpoint='actualizar_objetivo_general')
@login_required
@admin_required
def actualizar_objetivo_general():
    taller_id = request.form['taller_id']
    taller = Taller.query.get_or_404(taller_id)

    objetivo_general = request.form['objetivo_general']
    taller.objetivo_general = objetivo_general

    db.session.commit()
    flash('Objetivo general actualizado exitosamente.')

    return redirect(url_for('admin.planificacion_admin.listar_planificaciones_taller', taller_id=taller_id))
