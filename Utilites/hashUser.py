from werkzeug.security import generate_password_hash

password = '19406727-5'
hashed_password = generate_password_hash(password)
print(f'Tu clase es: {hashed_password}')
