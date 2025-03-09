from fastapi import FastAPI, HTTPException
import pika
import json

app = FastAPI()

# Configuration RabbitMQ
RABBITMQ_HOST = "localhost"
QUEUE_NAME = "user_update_queue"

def send_message_to_queue(message):
    """Envoie un message à la file d'attente RabbitMQ."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)  # Rend le message persistant
    )
    connection.close()

@app.post("/orders/")
def create_order(user_id: int):
    # Simuler la création d'une commande
    order_data = {
        "order_id": 101,
        "user_id": user_id,
        "status": "En cours"
    }

    # Envoyer un message pour mettre à jour l'utilisateur
    update_message = {
        "user_id": user_id,
        "update": {"last_order_id": 101}
    }
    send_message_to_queue(update_message)

    return {"message": "Commande créée avec succès", "order": order_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)