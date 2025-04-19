from detector_acoso import app, db, Usuario

# Crear un nuevo usuario
nuevo_usuario = Usuario(nombre="alex", correo="alex@correo.com", contraseña="alex6090")

# Usar el contexto de la app
with app.app_context():
    db.session.add(nuevo_usuario)
    db.session.commit()
    print("✅ Usuario creado con éxito.")
