from flask import Blueprint
from .docente import docente_bp


# Importar los Blueprints específicos de los docentes
from app.routes.user.docente_perfil import perfil_bp
from app.routes.user.docente_bitacoras import bitacoras_bp
from app.routes.user.docente_objetivos import objetivo_bp
from app.routes.user.docente_planificaciones import planificacion_bp

# Registrar los Blueprints específicos dentro del Blueprint principal de los docentes
docente_bp.register_blueprint(perfil_bp, url_prefix='/perfil')
docente_bp.register_blueprint(bitacoras_bp, url_prefix='/bitacoras')
docente_bp.register_blueprint(objetivo_bp, url_prefix='/objetivos')
docente_bp.register_blueprint(planificacion_bp, url_prefix='/planificaciones')
