from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime

from app.routes.admin.decorators import admin_required
from ...models import Clase, EstudianteTaller, AsistenciaEstudiante, Taller
from ...extensions import db

asistencias_bp = Blueprint('asistencias_admin', __name__)
@asistencias_bp.route('/', endpoint='asistencia_dashboard')
@login_required
@admin_required
def asistencia_dashboard():
    talleres = Taller.query.all()
    report_data = []

    for taller in talleres:
        clases = Clase.query.filter_by(taller_id=taller.taller_id).all()
        for clase in clases:
            total_estudiantes = EstudianteTaller.query.filter_by(taller_id=taller.taller_id).count()
            asistencias = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase).all()
            presentes = sum(1 for a in asistencias if a.presencia)
            ausentes = total_estudiantes - presentes
            porcentaje_asistencia = (presentes / total_estudiantes) * 100 if total_estudiantes else 0

            report_data.append({
                'fecha': clase.fecha,
                'taller': taller.nombre,
                'taller_id': taller.taller_id,
                'clase_id': clase.id_clase,
                'total': total_estudiantes,
                'presentes': presentes,
                'ausentes': ausentes,
                'porcentaje_asistencia': porcentaje_asistencia
            })

    return render_template('admin/asistencias_dashboard.html', report_data=report_data, talleres=talleres)

@asistencias_bp.route('/select_clase', methods=['GET', 'POST'], endpoint='select_clase')
@login_required
@admin_required
def select_clase():
    if request.method == 'POST':
        id_clase = request.form['id_clase']
        return redirect(url_for('admin.asistencias_admin.take_attendance', id_clase=id_clase))
    clases = Clase.query.options(db.joinedload(Clase.taller)).all()
    return render_template('admin/select_clase.html', clases=clases)

@asistencias_bp.route('/<int:id_clase>', methods=['GET', 'POST'], endpoint='take_attendance')
@login_required
@admin_required
def take_attendance(id_clase):
    clase = Clase.query.get_or_404(id_clase)
    estudiantes_taller = EstudianteTaller.query.filter_by(taller_id=clase.taller_id).all()
    estudiantes = [et.estudiante for et in estudiantes_taller]

    if request.method == 'POST':
        for estudiante in estudiantes:
            presencia = f'presencia_{estudiante.id_estudiante}' in request.form
            justificacion = request.form.get(f'justificacion_{estudiante.id_estudiante}', '')

            asistencia = AsistenciaEstudiante.query.filter_by(id_clase=id_clase, id_estudiante=estudiante.id_estudiante).first()
            if asistencia:
                asistencia.presencia = presencia
                asistencia.justificacion = justificacion
            else:
                nueva_asistencia = AsistenciaEstudiante(
                    id_clase=id_clase,
                    id_estudiante=estudiante.id_estudiante,
                    presencia=presencia,
                    justificacion=justificacion
                )
                db.session.add(nueva_asistencia)
        
        comentario_bitacora = request.form.get('comentario_bitacora')
        clase.comentario_bitacora = comentario_bitacora
        db.session.commit()
        
        return redirect(url_for('admin.asistencias_admin.asistencia_dashboard'))

    asistencias = {a.id_estudiante: a for a in AsistenciaEstudiante.query.filter_by(id_clase=id_clase).all()}
    return render_template('admin/take_attendance.html', clase=clase, estudiantes=estudiantes, asistencias=asistencias)

@asistencias_bp.route('/attendance_details/<int:id_clase>', endpoint='attendance_details')
@login_required
@admin_required
def attendance_details(id_clase):
    clase = Clase.query.get_or_404(id_clase)
    asistencias = AsistenciaEstudiante.query.filter_by(id_clase=id_clase).all()
    estudiantes_presentes = [a.estudiante for a in asistencias if a.presencia]
    estudiantes_ausentes = [a.estudiante for a in asistencias if not a.presencia]
    return render_template('admin/attendance_details.html', clase=clase, estudiantes_presentes=estudiantes_presentes, estudiantes_ausentes=estudiantes_ausentes)


@asistencias_bp.route('/monthly_report', methods=['GET', 'POST'], endpoint='monthly_report')
@login_required
@admin_required
def monthly_report():
    talleres = Taller.query.all()
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        taller_id = request.form['taller_id']
        return redirect(url_for('admin.asistencias_admin.view_monthly_report', start_date=start_date, end_date=end_date, taller_id=taller_id))
    return render_template('admin/monthly_report.html', talleres=talleres)

@asistencias_bp.route('/view_monthly_report', endpoint='view_monthly_report')
@login_required 
@admin_required
def view_monthly_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    taller_id = request.args.get('taller_id')

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

    clases = Clase.query.filter(Clase.fecha.between(start_date_obj, end_date_obj), Clase.taller_id == taller_id).all()
    
    monthly_data = {}
    for clase in clases:
        mes = clase.fecha.strftime('%B %Y')
        if mes not in monthly_data:
            monthly_data[mes] = {
                'clases': [],
                'total_estudiantes': 0,
                'total_presentes': 0,
                'total_clases': 0
            }
        total_estudiantes_clase = EstudianteTaller.query.filter_by(taller_id=clase.taller_id).count()
        asistencias = AsistenciaEstudiante.query.filter_by(id_clase=clase.id_clase).all()
        presentes = sum(1 for a in asistencias if a.presencia)
        ausentes = total_estudiantes_clase - presentes

        monthly_data[mes]['clases'].append({
            'fecha': clase.fecha,
            'presentes': presentes,
            'ausentes': ausentes,
            'comentario_bitacora': clase.comentario_bitacora
        })
        monthly_data[mes]['total_estudiantes'] += total_estudiantes_clase
        monthly_data[mes]['total_presentes'] += presentes
        monthly_data[mes]['total_clases'] += 1

    for mes, data in monthly_data.items():
        if data['total_estudiantes'] > 0 and data['total_clases'] > 0:
            data['porcentaje_asistencia'] = (data['total_presentes'] / (data['total_estudiantes'] * data['total_clases'])) * 100
        else:
            data['porcentaje_asistencia'] = 0

    return render_template('admin/view_monthly_report.html', monthly_data=monthly_data, start_date=start_date, end_date=end_date)
