from detector_acoso import app, db, Captura

with app.app_context():
    capturas = Captura.query.all()
    for captura in capturas:
        if captura.ruta_imagen.startswith("static/"):
            # Elimina 'static/' del inicio
            nueva_ruta = captura.ruta_imagen.replace("static/", "", 1)
            print(f"Corrigiendo: {captura.ruta_imagen} → {nueva_ruta}")
            captura.ruta_imagen = nueva_ruta
    db.session.commit()
    print("✅ Rutas corregidas correctamente.")
