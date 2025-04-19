import sys
import os
import cv2
import numpy as np
import torch
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
from flask_sqlalchemy import SQLAlchemy

# 👇 Hacemos que Python pueda importar desde yolov5/
sys.path.append(os.path.join(os.path.dirname(__file__), 'yolov5'))

# 👇 Imports de YOLOv5 (¡ya funcionan!)
from models.common import DetectMultiBackend
from utils.general import non_max_suppression
from utils.augmentations import letterbox

app = Flask(__name__)
app.secret_key = '2102'

# ✅ Configuración PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://alex:alex123@localhost/acoso_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --------------------- MODELOS ---------------------
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)

class Captura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ruta_imagen = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# --------------------- RUTAS WEB ---------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(correo=correo, contraseña=contraseña).first()
        if usuario:
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            return redirect(url_for('camaras'))
        else:
            flash('❌ Credenciales inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('🔒 Has cerrado sesión correctamente')
    return redirect(url_for('login'))

@app.route('/camaras')
def camaras():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('camaras.html', nombre=session.get('usuario_nombre'))

@app.route('/capturas')
def capturas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    capturas = Captura.query.order_by(Captura.fecha.desc()).all()
    return render_template('capturas.html', capturas=capturas)

# --------------------- DETECCIÓN EN VIVO ---------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
modelo = DetectMultiBackend("acoso.pt", device=device, dnn=False)
camera = cv2.VideoCapture(0)

def generar_stream():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Preprocesamiento para el modelo
        img = letterbox(frame, 640, stride=32, auto=True)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR → RGB → CHW
        img = np.ascontiguousarray(img)
        img_tensor = torch.from_numpy(img).to(device).float() / 255.0
        img_tensor = img_tensor.unsqueeze(0)

        # Inferencia
        pred = modelo(img_tensor)
        pred = non_max_suppression(pred, conf_thres=0.5, iou_thres=0.45)

        for det in pred:
            if len(det):
                # Dibujar los cuadros
                for *xyxy, conf, cls in det:
                    label = f"Detectado {conf:.2f}"
                    x1, y1, x2, y2 = map(int, xyxy)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)  # rojo
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                # Guardar la captura si hay detección
                guardar_captura(frame)
                notificar()
                break

        # Codificar y enviar el frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return Response(generar_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --------------------- UTILIDADES ---------------------
def guardar_captura(frame):
    nombre_archivo = f"captura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    ruta = os.path.join("static/capturas", nombre_archivo)
    cv2.imwrite(ruta, frame)
    nueva = Captura(ruta_imagen=ruta)
    db.session.add(nueva)
    db.session.commit()

def notificar():
    print("⚠️ Alerta: Se detectó comportamiento sospechoso")

# --------------------- MAIN ---------------------
if __name__ == '__main__':
    if not os.path.exists("static/capturas"):
        os.makedirs("static/capturas")
    app.run(debug=True)
