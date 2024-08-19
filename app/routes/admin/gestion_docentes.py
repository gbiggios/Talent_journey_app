from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from werkzeug.security import generate_password_hash
from app.models import DOCENTE, User
from app.extensions import db
from app.routes.admin.decorators import admin_required
from app.forms import DocenteForm, EditDocenteForm

docentes_bp = Blueprint('docentes_admin', __name__)

@docentes_bp.route('/', methods=['GET'], endpoint='docentes_admin_home')
@login_required
@admin_required
def docentes():
    form = DocenteForm()
    
    filter_type = request.args.get('filter', 'all')
    page = request.args.get('page', 1, type=int)

    if filter_type == 'active':
        docentes_query = DOCENTE.query.filter_by(activo=True)
    elif filter_type == 'inactive':
        docentes_query = DOCENTE.query.filter_by(activo=False)
    else:
        docentes_query = DOCENTE.query

    docentes_pagination = docentes_query.paginate(page=page, per_page=10)


    return render_template('admin/docentes.html', docentes_pagination=docentes_pagination, form=form)


@docentes_bp.route('/create', methods=['POST'], endpoint='docentes_admin_create')
@login_required
@admin_required
def create_docente():
    form = DocenteForm()
    if form.validate_on_submit():
        try:
            rut_docente = form.rut_docente.data
            existing_docente = DOCENTE.query.filter_by(rut_docente=rut_docente).first()
            if existing_docente:
                flash('El RUT ya está registrado. Por favor, ingrese un RUT diferente.', 'danger')
            else:
                # Generar la contraseña encriptada basada en el RUT
                contraseña_encriptada = generate_password_hash(rut_docente, method='pbkdf2:sha256')
                
                # Crear el nuevo objeto DOCENTE con la contraseña encriptada
                nuevo_docente = DOCENTE(
                    rut_docente=rut_docente,
                    nombre=form.nombre.data,
                    apellido_paterno=form.apellido_paterno.data,
                    apellido_materno=form.apellido_materno.data,
                    telefono=form.telefono.data,
                    correo=form.correo.data,
                    contraseña=contraseña_encriptada,  # Contraseña basada en el RUT
                    activo=True
                )

                db.session.add(nuevo_docente)
                db.session.commit()

                # Crear un nuevo usuario asociado al docente con el mismo RUT como nombre de usuario y contraseña
                nuevo_usuario = User(
                    username=rut_docente,
                    password=contraseña_encriptada,
                    id_docente=nuevo_docente.id_docente
                )

                db.session.add(nuevo_usuario)
                db.session.commit()

                flash('Docente y usuario agregados exitosamente.', 'success')
                return redirect(url_for('admin.docentes_admin.docentes_admin_home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Ocurrió un error al guardar el docente: {str(e)}', 'danger')
    else:
        flash('Por favor, corrija los errores en el formulario.', 'danger')

    # Si el formulario no es válido o hay un error, renderizar la misma página con los errores.
    return render_template('admin/docentes.html', form=form, docentes_pagination=DOCENTE.query.paginate(per_page=10))



@docentes_bp.route('/edit/<int:id_docente>', methods=['GET', 'POST'], endpoint='docentes_admin_edit')
@login_required
@admin_required
def edit_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    form = EditDocenteForm(obj=docente)
    if form.validate_on_submit():
        docente.rut_docente = form.rut_docente.data
        docente.nombre = form.nombre.data
        docente.apellido_paterno = form.apellido_paterno.data
        docente.apellido_materno = form.apellido_materno.data
        docente.telefono = form.telefono.data
        docente.correo = form.correo.data
        docente.contraseña = generate_password_hash(form.rut_docente.data, method='pbkdf2:sha256')
        db.session.commit()
        flash('Docente actualizado exitosamente.', 'success')
        return redirect(url_for('admin.docentes_admin.docentes_admin_home'))
    return render_template('admin/docentes.html', form=form, docentes_pagination=DOCENTE.query.paginate(per_page=10))

@docentes_bp.route('/delete/<int:id_docente>', methods=['POST'], endpoint='docentes_admin_delete')
@login_required
@admin_required
def delete_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    db.session.delete(docente)
    db.session.commit()
    flash('Docente eliminado exitosamente.', 'success')
    return redirect(url_for('docentes_admin.docentes_admin_home'))

@docentes_bp.route('/toggle_active/<int:id_docente>', methods=['POST'], endpoint='docentes_admin_toggle_active')
@login_required
@admin_required
def toggle_active_docente(id_docente):
    docente = DOCENTE.query.get_or_404(id_docente)
    docente.activo = not docente.activo
    db.session.commit()
    flash(f'Docente {"activado" if docente.activo else "desactivado"} exitosamente.', 'success')
    return redirect(url_for('admin.docentes_admin.docentes_admin_home'))
