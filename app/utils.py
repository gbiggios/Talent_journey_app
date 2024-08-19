# app/utils.py
import pandas as pd
import os
from . import db
from .models import Estudiantes

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['xls', 'xlsx']

def cargar_datos_excel(filepath):
    df = pd.read_excel(filepath)
    for index, row in df.iterrows():
        nuevo_estudiante = Estudiantes(
            rut_estudiante=row['rut_estudiante'],
            nombre=row['nombre'],
            apellido_paterno=row['apellido_paterno'],
            apellido_materno=row['apellido_materno'],
            curso=row['curso'],
            correo_institucional=row['correo_institucional']
        )
        db.session.add(nuevo_estudiante)
    db.session.commit()
    os.remove(filepath)
