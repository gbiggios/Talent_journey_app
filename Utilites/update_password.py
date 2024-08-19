import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from werkzeug.security import generate_password_hash
from app import create_app
from app.models import User, db

app = create_app()

with app.app_context():
    user = User.query.filter_by(username='13366469-6').first()
    if user:
        new_password_hash = generate_password_hash('13366469-6', method='pbkdf2:sha256')
        user.password = new_password_hash
        db.session.commit()
        print(f'Contraseña para el usuario {user.username} actualizada correctamente.')
