import requests

ORDER_SERVICE_URL = "http://127.0.0.1:8002/orders/"

# Liste des utilisateurs à tester
user_ids = [1, 2]

for user_id in user_ids:
    response = requests.get(f"{ORDER_SERVICE_URL}{user_id}")
    if response.status_code == 200:
        print(f"Commande pour l'utilisateur {user_id} :", response.json())
    else:
        print(f"Erreur pour l'utilisateur {user_id} :", response.json())
