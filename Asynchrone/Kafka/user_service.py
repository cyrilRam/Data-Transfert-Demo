from confluent_kafka import Consumer, KafkaError
import json

# Base d'utilisateurs fictive
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "last_order_id": None},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "last_order_id": None}
}

def update_user(user_id: int, update_data: dict):
    """Met à jour les informations de l'utilisateur."""
    if user_id in users_db:
        users_db[user_id].update(update_data)
        print(f"Utilisateur {user_id} mis à jour : {users_db[user_id]}")
    else:
        print(f"Utilisateur {user_id} non trouvé")

# Configuration Kafka
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "user_updates"

# Configuration du consommateur Kafka
consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": "user_service_group",
    "auto.offset.reset": "earliest"
})
consumer.subscribe([TOPIC_NAME])

def start_consumer():
    """Démarre le consommateur Kafka."""
    print("En attente de messages. Pour quitter, appuyez sur CTRL+C")
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Erreur Kafka : {msg.error()}")
                    break

            # Traiter le message
            message_value = json.loads(msg.value().decode("utf-8"))
            user_id = message_value["user_id"]
            update_data = message_value["update"]
            update_user(user_id, update_data)

    except KeyboardInterrupt:
        print("Arrêt du consommateur...")
    finally:
        consumer.close()

if __name__ == "__main__":
    start_consumer()