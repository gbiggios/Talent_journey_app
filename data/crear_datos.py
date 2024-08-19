import pandas as pd

# Datos de prueba
data = {
    'rut_estudiante': [
        '12345678-9', '98765432-1', '11111111-1', '22222222-2', '33333333-3', 
        '44444444-4', '55555555-5', '66666666-6', '77777777-7', '88888888-8',
        '99999999-9', '10101010-1', '20202020-2', '30303030-3', '40404040-4',
        '50505050-5', '60606060-6', '70707070-7', '80808080-8', '90909090-9'
    ],
    'nombre': [
        'Juan', 'María', 'Pedro', 'Ana', 'Luis',
        'Elena', 'Carlos', 'Marta', 'José', 'Lucía',
        'Raúl', 'Sofía', 'Miguel', 'Laura', 'Javier',
        'Isabel', 'Andrés', 'Carmen', 'Fernando', 'Patricia'
    ],
    'apellido_paterno': [
        'Pérez', 'Ramírez', 'González', 'Fernández', 'López',
        'Martínez', 'Sánchez', 'Gómez', 'Díaz', 'Torres',
        'Vargas', 'Rojas', 'Castro', 'Mendoza', 'Reyes',
        'Ortiz', 'Morales', 'Silva', 'Ramos', 'Romero'
    ],
    'apellido_materno': [
        'Gómez', 'Soto', 'Hernández', 'Jiménez', 'Ruiz',
        'Gutiérrez', 'Navarro', 'Flores', 'Espinoza', 'Valencia',
        'Carrillo', 'Paredes', 'Salazar', 'Cruz', 'Guerrero',
        'Delgado', 'Ortiz', 'Rivas', 'Mejía', 'Campos'
    ],
    'curso': [
        '4to A', '3ro B', '2do C', '1ro D', '5to E',
        '6to F', '7mo G', '8vo H', '9no I', '10mo J',
        '11vo K', '12vo L', '13vo M', '14vo N', '15vo O',
        '16vo P', '17vo Q', '18vo R', '19vo S', '20vo T'
    ],
    'correo_institucional': [
        'juan.perez@instituto.cl', 'maria.ramirez@instituto.cl', 'pedro.gonzalez@instituto.cl', 'ana.fernandez@instituto.cl', 'luis.lopez@instituto.cl',
        'elena.martinez@instituto.cl', 'carlos.sanchez@instituto.cl', 'marta.gomez@instituto.cl', 'jose.diaz@instituto.cl', 'lucia.torres@instituto.cl',
        'raul.vargas@instituto.cl', 'sofia.rojas@instituto.cl', 'miguel.castro@instituto.cl', 'laura.mendoza@instituto.cl', 'javier.reyes@instituto.cl',
        'isabel.ortiz@instituto.cl', 'andres.morales@instituto.cl', 'carmen.silva@instituto.cl', 'fernando.ramos@instituto.cl', 'patricia.romero@instituto.cl'
    ]
}

# Crear DataFrame
df = pd.DataFrame(data)

# Guardar como archivo Excel
df.to_excel('/mnt/data/estudiantes_prueba.xlsx', index=False)
