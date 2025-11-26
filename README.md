# Instalación rápida

## 1. Instalar dependencias
Asegurate de estar dentro de la carpeta del proyecto y ejecutar:

📌 Proyecto Django — Instalación Rápida

Este proyecto está desarrollado con Django 5 y usa los siguientes paquetes principales:

-asgiref==3.10.0
-Django==5.2.7
-graphviz==0.21
-pillow==12.0.0
-sqlparse==0.5.3
-tzdata==2025.2
# Instalación rápida

git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
