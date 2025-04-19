# 🎥 Sistema de Detección de Acoso con Flask + YOLOv8

Este es un sistema web que utiliza **Flask** y el modelo **YOLOv8 (`acoso.pt`)** para detectar comportamientos sospechosos en tiempo real usando la cámara de tu PC. Incluye funcionalidades de login, visualización en vivo, registro de capturas y alertas básicas.

---

## 🚀 Funcionalidades

- 🔐 Inicio y cierre de sesión seguro
- 🎥 Transmisión en vivo desde la cámara de tu PC
- 🤖 Detección automática de comportamientos sospechosos usando YOLO
- 🖼️ Registro y visualización de capturas clasificadas
- 📦 Base de datos PostgreSQL para usuarios y eventos

---

## 🧪 Usuario de prueba

| Correo               | Contraseña |
|----------------------|------------|
| alex@correo.com      | alex6090   |

---

## ⚙️ Requisitos

- Python 3.10+
- PostgreSQL
- `acoso.pt` (modelo YOLOv5 entrenado)
- Librerías de Python:

```bash
pip install -r requirements.txt
