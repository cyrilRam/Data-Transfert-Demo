import asyncio
import websockets
import json

async def send_order(user_id: int, order_id: int):
    """Envoie une commande au service Order via WebSocket."""
    uri = "ws://localhost:8002/ws/order"
    async with websockets.connect(uri) as websocket:
        order_data = {
            "user_id": user_id,
            "order_id": order_id
        }
        await websocket.send(json.dumps(order_data))
        response = await websocket.recv()
        print("Réponse du service Order :", response)

if __name__ == "__main__":
    user_id = 1
    order_id = 101
    print(f"Création d'une commande pour l'utilisateur {user_id}...")
    asyncio.get_event_loop().run_until_complete(send_order(user_id, order_id))