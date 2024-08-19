from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    id_docente = db.Column(db.Integer, db.ForeignKey('docente.id_docente'), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @property
    def is_docente(self):
        return self.id_docente is not None

    def get_id(self):
        return self.id
    
class DOCENTE(db.Model):
    id_docente = db.Column(db.Integer, primary_key=True)
    rut_docente = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    contraseña = db.Column(db.String(150), nullable=False)
    activo = db.Column(db.Boolean, default=True)

    user = db.relationship('User', backref='docente', lazy=True)

    def set_password(self, password):
        self.contraseña = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

class Sala(db.Model):
    id_sala = db.Column(db.Integer, primary_key=True)
    nombre_sala = db.Column(db.String(50), nullable=False)

class Taller(db.Model):
    taller_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    horario = db.Column(db.String(50), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id_sala'), nullable=False)
    id_docente = db.Column(db.Integer, db.ForeignKey('docente.id_docente'), nullable=False)
    objetivo_general = db.Column(db.String(200), nullable=False)

    sala = db.relationship('Sala', backref=db.backref('talleres', lazy=True))
    docente = db.relationship('DOCENTE', backref=db.backref('talleres', lazy=True))
    estudiantes_taller = db.relationship('EstudianteTaller', backref='taller', lazy=True)
    clases = db.relationship('Clase', back_populates='taller')

class Estudiantes(db.Model):
    id_estudiante = db.Column(db.Integer, primary_key=True)
    rut_estudiante = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    curso = db.Column(db.String(20))
    correo_institucional = db.Column(db.String(100))

    talleres = db.relationship('EstudianteTaller', backref='estudiante', lazy=True)

class EstudianteTaller(db.Model):
    id_taller_estudiante = db.Column(db.Integer, primary_key=True)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.taller_id'), nullable=False)

class Clase(db.Model):
    __tablename__ = 'clase'
    
    id_clase = db.Column(db.Integer, primary_key=True)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.taller_id'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    comentario_bitacora = db.Column(db.Text, nullable=True)
    
    taller = db.relationship('Taller', back_populates='clases')

class AsistenciaEstudiante(db.Model):
    id_asistencia = db.Column(db.Integer, primary_key=True)
    id_clase = db.Column(db.Integer, db.ForeignKey('clase.id_clase'), nullable=False)
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'), nullable=False)
    presencia = db.Column(db.Boolean, nullable=False)
    justificacion = db.Column(db.Text)

    clase = db.relationship('Clase', backref=db.backref('asistencias', lazy=True))
    estudiante = db.relationship('Estudiantes', backref=db.backref('asistencias', lazy=True))

class Planificacion(db.Model):
    __tablename__ = 'planificacion'

    id_planificacion = db.Column(db.Integer, primary_key=True)
    taller_id = db.Column(db.Integer, db.ForeignKey('taller.taller_id'), nullable=False)
    mes = db.Column(db.String(50), nullable=False)  # Mes de la planificación
    habilidades = db.Column(db.Text, nullable=True)  # Habilidades trabajadas en el mes
    recursos = db.Column(db.Text, nullable=True)  # Recursos utilizados en el mes
    actividades = db.Column(db.Text, nullable=True)  # Descripción de las actividades del mes
    estado = db.Column(db.String(20), nullable=False, default="No realizado")  # Estado de la planificación
    
    taller = db.relationship('Taller', backref=db.backref('planificaciones', lazy=True))
