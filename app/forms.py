from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from app.models import Estudiantes, Taller

class LoginForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])


class DocenteForm(FlaskForm):
    rut_docente = StringField('RUT Docente', validators=[DataRequired(), Length(min=5, max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=2, max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(min=2, max=50)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=9, max=15)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    activo = BooleanField('Activo')
    submit = SubmitField('Guardar')


class EditDocenteForm(FlaskForm):
    rut_docente = StringField('RUT Docente', validators=[DataRequired(), Length(min=5, max=20)])
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=2, max=50)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(min=2, max=50)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(min=7, max=15)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Actualizar')


class SalaForm(FlaskForm):
    nombre_sala = StringField('Nombre de la Sala', validators=[DataRequired()])

class TallerForm(FlaskForm):
    nombre = StringField('Nombre del Taller', validators=[DataRequired()])
    horario = SelectField('Horario', choices=[
        ('Lunes 17:00-18:00', 'Lunes 17:00-18:00'),
        ('Lunes 19:30-20:30', 'Lunes 19:30-20:30'),
        ('Martes 17:00-18:00', 'Martes 17:00-18:00'),
        ('Martes 19:30-20:30', 'Martes 19:30-20:30'),
        ('Miércoles 17:00-18:00', 'Miércoles 17:00-18:00'),
        ('Miércoles 19:30-20:30', 'Miércoles 19:30-20:30'),
        ('Jueves 17:00-18:00', 'Jueves 17:00-18:00'),
        ('Jueves 19:30-20:30', 'Jueves 19:30-20:30')
    ], validators=[DataRequired()])
    id_sala = SelectField('Sala', coerce=int, validators=[DataRequired()])
    id_docente = SelectField('Docente', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar cambios')

class EstudiantesForm(FlaskForm):
    rut_estudiante = StringField('RUT Estudiante', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired()])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired()])
    curso = StringField('Curso', validators=[DataRequired()])
    correo_institucional = StringField('Correo Institucional', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar Estudiante')


class ClaseForm(FlaskForm):
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    comentario_bitacora = TextAreaField('Comentario de Bitácora')
    submit = SubmitField('Guardar Clase')


class PlanificacionForm(FlaskForm):
    mes = StringField('Mes', validators=[DataRequired()])
    habilidades = TextAreaField('Habilidades')
    recursos = TextAreaField('Recursos')
    actividades = TextAreaField('Actividades')
    estado = SelectField('Estado', choices=[
        ('No realizado', 'No realizado'),
        ('En desarrollo', 'En desarrollo'),
        ('Planificado', 'Planificado')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar Planificación')

class AsistenciaEstudianteForm(FlaskForm):
    presencia = BooleanField('Presencia', validators=[DataRequired()])
    justificacion = TextAreaField('Justificación')
    submit = SubmitField('Guardar Asistencia')


class EstudianteTallerForm(FlaskForm):
    id_estudiante = SelectField('Selecciona un Estudiante', coerce=int, validators=[DataRequired()])
    taller_id = SelectField('Selecciona un Taller', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Estudiante al Taller')

    def __init__(self, *args, **kwargs):
        super(EstudianteTallerForm, self).__init__(*args, **kwargs)
        
        # Poblar las opciones de los select fields ordenadas alfabéticamente
        self.id_estudiante.choices = sorted(
            [(estudiante.id_estudiante, f"{estudiante.nombre} {estudiante.apellido_paterno}") for estudiante in Estudiantes.query.all()],
            key=lambda x: x[1]  # Ordena por nombre completo
        )
        
        self.taller_id.choices = sorted(
            [(taller.taller_id, taller.nombre) for taller in Taller.query.all()],
            key=lambda x: x[1]  # Ordena por nombre del taller
        )