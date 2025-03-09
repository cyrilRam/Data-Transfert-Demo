import requests

# URL du service Order
ORDER_SERVICE_URL = "http://127.0.0.1:8002/orders/"

def create_order(user_id: int):
    """Envoie une requête POST pour créer une commande."""
    try:
        response = requests.post(ORDER_SERVICE_URL, params={"user_id": user_id})
        if response.status_code == 200:
            print("Réponse du service Order :")
            print(response.json())
        else:
            print(f"Erreur : {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête : {e}")

if __name__ == "__main__":
    # Simuler la création d'une commande pour l'utilisateur 1
    user_id = 1
    print(f"Création d'une commande pour l'utilisateur {user_id}...")
    create_order(user_id)