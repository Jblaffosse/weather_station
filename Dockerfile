# ==================================================
# Program Name: Weather Station
# Description:
#     Configuration file to execute the application using Docker
#
# Author: JB LAFFOSSE
# Date: 2025-02-24
# Version: 1.0.0
# License: None
# ==================================================

FROM python:3.11

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port utilisé par Flask (par défaut 5000)
EXPOSE 10500

# Exposer le port utilisé par le server UDP
EXPOSE 10501

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV FLASK_APP run.py
# ENV DEBUG True

# Définir la commande de lancement
CMD ["python", "weather_station.py"]
