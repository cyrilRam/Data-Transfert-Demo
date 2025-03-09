import pika
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

def callback(ch, method, properties, body):
    """Fonction appelée lorsqu'un message est reçu."""
    message = json.loads(body)
    user_id = message["user_id"]
    update_data = message["update"]
    update_user(user_id, update_data)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirme la réception du message

def start_consumer():
    """Démarre le consommateur RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="user_update_queue", durable=True)
    channel.basic_consume(queue="user_update_queue", on_message_callback=callback)
    print("En attente de messages. Pour quitter, appuyez sur CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()