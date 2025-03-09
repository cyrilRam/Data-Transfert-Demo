from zeep import Client

# URL du service de commande SOAP
ORDER_SERVICE_URL = "http://127.0.0.1:8002/?wsdl"

# Créer un client SOAP
client = Client(ORDER_SERVICE_URL)

# Appeler la méthode get_order avec user_id=1
try:
    response = client.service.get_order(1)
    print("Réponse du service de commande :")
    print(response)
except Exception as e:
    print("Erreur lors de l'appel du service de commande :", str(e))