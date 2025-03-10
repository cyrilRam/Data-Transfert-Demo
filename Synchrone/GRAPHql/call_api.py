import requests

# URL du serveur GraphQL
GRAPHQL_URL = "http://127.0.0.1:8003/graphql"

# Requête pour l'utilisateur 1 (on demande id, name et status de la commande)
query_user_1 = """
query {
    getOrder(orderId: 101) {
        orderId
        status
        user {
            id
            name
        }
    }
}
"""

# Requête pour l'utilisateur 2 (on demande id, email et status de la commande)
query_user_2 = """
query {
    getOrder(orderId: 102) {
        orderId
        status
        user {
            id
            email
        }
    }
}
"""

# Fonction pour exécuter une requête GraphQL
def execute_graphql_query(query):
    response = requests.post(GRAPHQL_URL, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Erreur lors de l'appel de l'API GraphQL"}

# Appels à l'API GraphQL
print("Résultat pour l'utilisateur 1 :")
result_user_1 = execute_graphql_query(query_user_1)
print(result_user_1)

print("\nRésultat pour l'utilisateur 2 :")
result_user_2 = execute_graphql_query(query_user_2)
print(result_user_2)