from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length

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