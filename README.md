# Medical Inventory Management System

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/med_inv_manage.git
cd med_inv_manage
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install Django==6.0.2
pip install django-crispy-forms==2.5
pip install crispy-bootstrap5==2025.6
pip install face-recognition==1.3.0
pip install face_recognition_models==0.3.0
pip install dlib==20.0.0
pip install mediapipe==0.10.32
pip install opencv-python==4.13.0.92
pip install ultralytics==8.4.18
pip install ollama==0.6.1
pip install torch==2.10.0
pip install torchvision==0.25.0
pip install numpy==2.4.2
pip install pillow==12.1.1
pip install setuptools==82.0.0
```

### 4. Running the Server

```bash
cd /home/emi_zabuntu/med_inv_manage67 && /home/emi_zabuntu/med_inv_manage67/world0/bin/uvicorn med_inv_manage.asgi:application --host 0.0.0.0 --port 8000 --ssl-keyfile key.pem --ssl-certfile cert.pem
#INSERT CORRECT PROJECT DIRECTORY
```
