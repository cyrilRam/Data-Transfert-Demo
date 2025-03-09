from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from zeep import Client


# Définition du modèle utilisateur basé sur le schéma XSD
class User(ComplexModel):
    __namespace__ = "http://example.com/user"
    id = Integer
    name = Unicode
    email = Unicode
    age = Integer(min_occurs=0)  # Optionnel


# URL du service utilisateur SOAP
USER_SERVICE_URL = "http://127.0.0.1:8001/?wsdl"


# Définition du service SOAP pour les commandes
class OrderService(ServiceBase):
    @rpc(Integer, _returns=Unicode)
    def get_order(ctx, user_id):
        # Appel du service utilisateur via SOAP
        client = Client(USER_SERVICE_URL)
        try:
            # Appel de la méthode get_user du service utilisateur
            user_data = client.service.get_user(user_id)

            # Afficher le résultat dans la console
            print("Réponse du service utilisateur :")
            print(user_data)

            # Retourner la réponse au client
            return f"<order><order_id>101</order_id><user>{user_data}</user><status>En cours</status></order>"
        except Exception as e:
            # Afficher l'erreur dans la console
            print("Erreur lors de la récupération de l'utilisateur :", str(e))
            return f"<error>Erreur lors de la récupération de l'utilisateur : {str(e)}</error>"


# Création de l'application SOAP
application = Application([OrderService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Serveur WSGI
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8002, wsgi_application)
    print("Service de commande SOAP démarré sur http://127.0.0.1:8002")
    print("WSDL disponible à : http://127.0.0.1:8002/?wsdl")
    server.serve_forever()