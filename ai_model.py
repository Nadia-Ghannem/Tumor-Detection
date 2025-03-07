import os
import tensorflow as tf
import logging

# Configurer les logs
logging.basicConfig(
    level=logging.INFO
)  # Changer à DEBUG pour des détails supplémentaires
logger = logging.getLogger(__name__)

# Réduire les logs TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Chemin absolu du modèle
MODEL_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "models", "tumor_model.h5")
)

# Charger le modèle une fois au démarrage
try:
    MODEL = tf.keras.models.load_model(MODEL_PATH)
    logger.info(f"Modèle chargé avec succès depuis : {MODEL_PATH}")
except Exception as e:
    logger.error(f"Erreur lors du chargement du modèle : {str(e)}")
    raise


def detect_tumor(image_path):
    try:
        # Vérification si l'image existe
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image introuvable : {image_path}")

        # Charger et prétraiter l'image
        image = tf.keras.utils.load_img(
            image_path, target_size=(224, 224)
        )  # Assurez-vous que la taille correspond au modèle
        input_array = tf.keras.utils.img_to_array(image) / 255.0
        input_array = tf.expand_dims(input_array, axis=0)

        # Prédiction
        prediction = MODEL.predict(input_array)
        logger.debug(f"Prédiction brute : {prediction}")

        confidence = float(prediction[0][0])  # Convertir en float
        result = "Tumor Detected" if confidence > 0.5 else "No Tumor"

        logger.debug(f"Résultat : {result}, Confiance : {confidence}")
        return result, confidence

    except Exception as e:
        logger.error(f"Erreur lors de la détection de la tumeur : {str(e)}")
        raise
