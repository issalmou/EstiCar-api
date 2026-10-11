---
title: EstiCar API
emoji: 🚗
colorFrom: red
colorTo: green
sdk: docker
pinned: false
---

# EstiCar API

API REST développée avec **Flask** pour estimer le prix de véhicules d'occasion et proposer des véhicules similaires à partir de données issues d'annonces automobiles.

L'application utilise un modèle de machine learning **Random Forest**, un préprocesseur sérialisé avec `joblib` et des jeux de données CSV. Elle est configurée pour être déployée sur **Hugging Face Spaces** avec Docker.

## Fonctionnalités

- Estimation du prix d'un véhicule à partir de ses caractéristiques.
- Retour d'une sélection de véhicules disponibles.
- Recherche de véhicules similaires par localisation, marque et modèle.
- API JSON compatible avec les applications web et mobiles.
- Support CORS disponible pour les intégrations frontend.
- Déploiement Docker sur le port `7860`.

## Technologies utilisées

- Python 3.9
- Flask
- Flask-CORS
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Docker
- Hugging Face Spaces

## Structure du projet

```text
.
├── app.py                    # Application Flask et routes API
├── model_random_forest.pkl   # Modèle Random Forest entraîné
├── preprocessor.pkl          # Préprocesseur des données d'entrée
├── moteurP.csv               # Données de véhicules
├── avito1.csv                # Données d'annonces automobiles
├── requirements.txt          # Dépendances Python
├── Dockerfile                # Configuration de l'image Docker
└── space.yaml                # Configuration Hugging Face Spaces
```

## Installation locale

### Prérequis

- Python 3.9 ou une version compatible
- `pip`
- Git

### Installation

```bash
git clone https://github.com/issalmou/EstiCar-api.git
cd EstiCar-api
python -m venv .venv
```

Activez ensuite l'environnement virtuel :

```bash
# Linux / macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Lancement de l'API

```bash
python app.py
```

L'API sera disponible à l'adresse suivante :

```text
http://localhost:7860
```

## Endpoints

### Estimer le prix d'un véhicule

```http
POST /predict
Content-Type: application/json
```

Exemple de requête :

```json
{
  "Marque": "Dacia",
  "Modèle": "Sandero",
  "Année": 2020,
  "Kilométrage": 45000,
  "Carburant": "Essence",
  "Boîte de vitesses": "Manuelle",
  "ABS": 1,
  "Airbags": 1,
  "Climatisation": 1,
  "Caméra de recul": 0,
  "GPS": 0
}
```

Les champs utilisés par le modèle doivent correspondre aux colonnes attendues par le préprocesseur enregistré dans `preprocessor.pkl`.

Exemple de réponse :

```json
{
  "predicted_price": 125000
}
```

### Récupérer des véhicules

```http
GET /list_voiture
```

Retourne un échantillon de six véhicules provenant du fichier `moteurP.csv`.

### Récupérer des véhicules similaires

```http
GET /list_voiture_similaire
```

Retourne jusqu'à trois véhicules issus de `avito1.csv`.

### Rechercher des véhicules similaires selon des critères

```http
POST /list_voiture_similaire
Content-Type: application/json
```

Exemple de requête :

```json
{
  "localisation": "Casablanca",
  "marque": "Dacia",
  "modele": "Sandero"
}
```

La recherche applique progressivement les filtres suivants :

1. Localisation, marque et modèle.
2. Marque et modèle.
3. Marque uniquement.
4. Un échantillon général si aucun résultat n'est trouvé.

## Utilisation avec Docker

Construire l'image :

```bash
docker build -t esticar-api .
```

Lancer le conteneur :

```bash
docker run --rm -p 7860:7860 esticar-api
```

L'API sera accessible sur `http://localhost:7860`.

## Déploiement sur Hugging Face Spaces

Le dépôt contient les fichiers nécessaires au déploiement :

- `Dockerfile` pour construire et lancer l'application.
- `space.yaml` pour déclarer l'application Flask.
- Le port `7860`, utilisé par Hugging Face Spaces.

Pour déployer le projet, créez un Space configuré avec le SDK **Docker**, puis connectez-le à ce dépôt ou poussez directement les fichiers du projet dans le Space.

## Remarques

- Les fichiers `*.pkl` doivent être présents à la racine du projet afin que l'application puisse charger le modèle et le préprocesseur.
- Les fichiers CSV sont chargés au moment de l'appel des endpoints correspondants.
- Pour une utilisation en production, il est recommandé d'ajouter une validation stricte des données d'entrée, une gestion centralisée des erreurs et une configuration CORS adaptée au domaine frontend autorisé.

## Licence

Aucune licence open source n'est actuellement déclarée pour ce projet.
