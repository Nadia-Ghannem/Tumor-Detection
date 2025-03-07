import paho.mqtt.client as mqtt
import json
import logging
from .models import TumorAnalysis, Patient

# Configuration du logger
logger = logging.getLogger("MQTTService")
logging.basicConfig(
    level=logging.DEBUG,  # INFO pour des logs moins détaillés
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def on_message(client, userdata, message):
    """Callback exécuté lorsqu'un message est reçu."""
    try:
        logger.info(f"Message reçu sur le topic : {message.topic}")
        logger.debug(f"Contenu brut du message : {message.payload.decode()}")

        # Charger et décoder le payload JSON
        payload = json.loads(message.payload.decode())
        logger.debug(f"Payload décodé : {payload}")

        # Validation des champs attendus
        patient_id = payload.get('patient_id')
        result = payload.get('result')
        confidence = payload.get('confidence')

        if not patient_id or result is None or confidence is None:
            logger.error(f"Format de payload invalide : {payload}")
            return

        # Sauvegarde des données dans la base
        try:
            patient = Patient.objects.get(id=patient_id)
            TumorAnalysis.objects.create(patient=patient, result=result, confidence_score=confidence)
            logger.info(f"Analyse sauvegardée avec succès pour le patient ID {patient_id}")
        except Patient.DoesNotExist:
            logger.error(f"Patient avec ID {patient_id} introuvable.")
        except Exception as db_error:
            logger.error(f"Erreur lors de la sauvegarde dans la base : {db_error}")

    except json.JSONDecodeError as decode_error:
        logger.error(f"Erreur de décodage JSON : {decode_error}")
    except Exception as e:
        logger.error(f"Erreur inattendue lors du traitement du message : {str(e)}")


def start_mqtt_service():
    """Démarre le service MQTT pour écouter les messages."""
    client = mqtt.Client()
    client.on_message = on_message  # Associer la fonction de callback

    # Connecter au broker MQTT
    try:
        client.connect("broker.hivemq.com", 1883, 60)
        logger.info("Connecté au broker MQTT")
    except Exception as e:
        logger.error(f"Erreur lors de la connexion au broker : {str(e)}")
        return

    # S'abonner au sujet
    try:
        client.subscribe("tumor_analysis/topic")
        logger.info("Abonné au topic 'tumor_analysis/topic'")
    except Exception as e:
        logger.error(f"Erreur lors de l'abonnement au topic : {str(e)}")
        return

    # Démarrer l'écoute des messages
    try:
        logger.info("Démarrage du listener MQTT...")
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        logger.info("Service MQTT arrêté.")
    except Exception as e:
        logger.error(f"Erreur inattendue dans le service MQTT : {str(e)}")
