from flask import Flask, redirect, url_for
from .extensions import db, csrf, login_manager  # Importa las extensiones desde el archivo extensions.py
from app.models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')  # Asegúrate de tener configuraciones adecuadas aquí

    # Inicializa las extensiones con la app
    db.init_app(app)
    csrf.init_app(app)  # Inicializa CSRF
    login_manager.init_app(app)

    # Configura el `user_loader`
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importa y registra tus blueprints
    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.routes.user import docente_bp
    app.register_blueprint(docente_bp, url_prefix='/docente')

    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Redirige la raíz al login
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app
