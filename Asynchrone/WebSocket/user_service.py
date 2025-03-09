import websockets
import asyncio
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

async def listen_to_order_service():
    """Écoute les mises à jour du service Order via WebSocket."""
    uri = "ws://localhost:8002/ws/order"
    async with websockets.connect(uri) as websocket:
        print("Connecté au service Order. En attente de mises à jour...")
        while True:
            message = await websocket.recv()
            update_message = json.loads(message)
            user_id = update_message["user_id"]
            update_data = update_message["update"]
            update_user(user_id, update_data)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_to_order_service())