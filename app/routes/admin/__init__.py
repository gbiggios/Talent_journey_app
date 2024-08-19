from .admin import admin_bp  # Importa el admin_bp desde admin.py

# Importar los sub-blueprints
from .gestion_docentes import docentes_bp
from .gestion_salas import salas_bp
from .gestion_talleres import talleres_bp
from .gestion_estudiantes import estudiantes_bp
from .gestion_clases import clases_bp
from .gestion_estudiante_taller import estudiantes_taller_bp
from .gestion_asistencia import asistencias_bp
from .gestionar_planificaciones import planificacion_bp
from .historial_asistencia import historial_bp
from .gestion_bitacora import bitacoras_bp
from .gestion_perfiles import gestion_perfiles_bp


# Registrar los sub-blueprints dentro del blueprint de admin
admin_bp.register_blueprint(docentes_bp, url_prefix='/docentes')
admin_bp.register_blueprint(salas_bp, url_prefix='/salas')
admin_bp.register_blueprint(talleres_bp, url_prefix='/talleres')
admin_bp.register_blueprint(estudiantes_bp, url_prefix='/estudiantes')
admin_bp.register_blueprint(clases_bp, url_prefix='/clases')
admin_bp.register_blueprint(estudiantes_taller_bp, url_prefix='/estudiantes_taller')
admin_bp.register_blueprint(asistencias_bp, url_prefix='/asistencias')
admin_bp.register_blueprint(planificacion_bp, url_prefix='/planificaciones')
admin_bp.register_blueprint(historial_bp, url_prefix='/historial')
admin_bp.register_blueprint(bitacoras_bp, url_prefix='/bitacoras')
admin_bp.register_blueprint(gestion_perfiles_bp, url_prefix='/perfiles')
