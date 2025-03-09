from fastapi import FastAPI, WebSocket
import asyncio

app = FastAPI()

# Liste des connexions WebSocket actives
active_connections = []

@app.websocket("/ws/order")
async def websocket_order(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Recevoir une commande du client
            data = await websocket.receive_json()
            user_id = data["user_id"]
            order_id = data["order_id"]

            # Simuler la création d'une commande
            order_data = {
                "order_id": order_id,
                "user_id": user_id,
                "status": "En cours"
            }

            # Envoyer une mise à jour au service User
            update_message = {
                "user_id": user_id,
                "update": {"last_order_id": order_id}
            }
            for connection in active_connections:
                await connection.send_json(update_message)

            # Répondre au client
            await websocket.send_json({"message": "Commande créée avec succès", "order": order_data})

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)