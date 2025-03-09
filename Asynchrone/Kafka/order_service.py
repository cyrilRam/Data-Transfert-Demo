from fastapi import FastAPI
from confluent_kafka import Producer
import json

app = FastAPI()

# Configuration Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "user_updates"

# Configuration du producteur Kafka
producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def delivery_report(err, msg):
    """Callback pour confirmer la livraison du message."""
    if err is not None:
        print(f"Échec de la livraison du message : {err}")
    else:
        print(f"Message livré à {msg.topic()} [{msg.partition()}]")

@app.post("/orders/")
def create_order(user_id: int):
    # Simuler la création d'une commande
    order_data = {
        "order_id": 101,
        "user_id": user_id,
        "status": "En cours"
    }

    # Créer un message pour mettre à jour l'utilisateur
    update_message = {
        "user_id": user_id,
        "update": {"last_order_id": 101}
    }

    # Publier le message dans Kafka
    producer.produce(
        TOPIC_NAME,
        key=str(user_id),
        value=json.dumps(update_message),
        callback=delivery_report
    )
    producer.flush()  # S'assurer que le message est envoyé

    return {"message": "Commande créée avec succès", "order": order_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)