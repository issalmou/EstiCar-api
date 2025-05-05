from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS
import joblib
import pandas as pd

app = Flask(__name__)
# CORS(app)  # <-- Autoriser toutes les origines

# Charger le modèle
model = joblib.load("model_random_forest.pkl")
preprocessor = joblib.load("preprocessor.pkl")


@app.route("/predict", methods=["POST"])
def predict():
    equipements = [
        "ABS",
        "Airbags",
        "CD/MP3/Bluetooth",
        "Caméra de recul",
        "Climatisation",
        "ESP",
        "Jantes aluminium",
        "Limiteur de vitesse",
        "Ordinateur de bord",
        "Radar de recul",
        "Régulateur de vitesse",
        "Sièges cuir",
        "Système de navigation/GPS",
        "Toit ouvrant",
        "Verrouillage centralisé à distance",
        "Vitres électriques",
    ]
    data = request.get_json()
    for i in equipements:
        data[i] = 1.0 if data.get(i) == 1 else 0.0

    data = pd.DataFrame([data])
    input_features = preprocessor.transform(data)
    prediction = model.predict(input_features)
    print(prediction)
    return jsonify({"predicted_price": np.round(float(prediction[0]))})


@app.route("/list_voiture", methods=["GET"])
def list_voiture():
    data = pd.read_csv("moteurP.csv")
    return data.sample(n=6).to_json(
        orient="records"
    )  # records pour retourner list of dictionnaire one per row


@app.route("/list_voiture_similaire", methods=["GET"])
def list_voiture_similaire():
    data = pd.read_csv("avito1.csv")
    return (
        data.sort_values(ascending=False, by="Prix")
        .sample(n=3)
        .to_json(orient="records")
    )


@app.route("/list_voiture_similaire", methods=["POST"])
def list_voiture_similaire_specifie():
    data_A = request.get_json()
    data = pd.read_csv("avito1.csv")
    filters = [
        (data["Localisation"].str.lower() == data_A["localisation"].lower())
        & (data["Marque"].str.lower() == data_A["marque"].lower())
        & (data["Modèle"].str.lower() == data_A["modele"].lower()),
        (data["Marque"].str.lower() == data_A["marque"].lower()) & (data["Modèle"].str.lower() == data_A["modele"].lower()),
        (data["Marque"].str.lower() == data_A["marque"].lower()),
    ]
    
    for f in filters:
        data_r = data[f]
        if not data_r.empty:
            return (
                data_r.sort_values(by="Prix", ascending=False)
                .sample(n=min(3, len(data_r)))
                .to_json(orient="records")
            )
    return (
        data.sort_values(by="Prix", ascending=False).sample(n=3).to_json(orient="records")
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
