import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Flatten

import os

print(tf.__version__)
# Définir le chemin où le modèle sera sauvegardé
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../models/tumor_model.h5")

#  création d'un modèle séquentiel
model = Sequential(
    [
        Flatten(input_shape=(224, 224, 3)),  # Entrée de taille 224x224x3 (images RGB)
        Dense(128, activation="relu"),  # Couche dense avec activation ReLU
        Dense(1, activation="sigmoid"),  # Couche de sortie pour classification binaire
    ]
)

# Compiler le modèle avec une fonction de perte adaptée
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Vérifier si le dossier pour sauvegarder le modèle existe, sinon le créer
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# Sauvegarder le modèle
model.save(MODEL_PATH)

print(f"Modèle sauvegardé avec succès à : {MODEL_PATH}")
