from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

# Définition du modèle utilisateur basé sur le schéma XSD
class User(ComplexModel):
    __namespace__ = "http://example.com/user"
    id = Integer
    name = Unicode
    email = Unicode
    age = Integer(min_occurs=0)  # Optionnel

# Base d'utilisateurs fictive
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 25}
}

# Définition du service SOAP
class UserService(ServiceBase):
    @rpc(Integer, _returns=User)
    def get_user(ctx, user_id):
        user = users_db.get(user_id)
        if user:
            return User(id=user["id"], name=user["name"], email=user["email"], age=user.get("age"))
        raise ValueError("Utilisateur non trouvé")

# Création de l'application SOAP
application = Application([UserService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

# Serveur WSGI
wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8001, wsgi_application)
    print("Service utilisateur SOAP démarré sur http://127.0.0.1:8001")
    print("WSDL disponible à : http://127.0.0.1:8001/?wsdl")
    server.serve_forever()