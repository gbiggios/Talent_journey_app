import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from werkzeug.security import generate_password_hash
from app import create_app
from app.models import User, db

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        # Verifica si la contraseña ya está en el formato pbkdf2:sha256
        if not user.password.startswith('pbkdf2:sha256'):
            print(f'Updating password for user {user.username}')
            # Actualiza la contraseña al formato pbkdf2:sha256
            new_password_hash = generate_password_hash(user.password, method='pbkdf2:sha256')
            user.password = new_password_hash
            db.session.commit()
    print("Contraseñas actualizadas correctamente.")
