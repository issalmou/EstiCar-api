# Étape 1 : Utiliser l'image officielle Python 3.9.21
FROM python:3.9.21-slim

# Étape 2 : Définir le dossier de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier les fichiers du projet vers le conteneur
COPY . .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Exposer le port 7860 (obligatoire pour Hugging Face Spaces)
EXPOSE 5000

# Étape 6 : Lancer l'application Flask
CMD ["python", "app.py"]
