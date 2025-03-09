from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
import strawberry

# Base d'utilisateurs fictive
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

# Base de commandes fictive
orders_db = {
    101: {"order_id": 101, "user_id": 1, "status": "En cours"},
    102: {"order_id": 102, "user_id": 2, "status": "Terminé"}
}

# Définition du type User
@strawberry.type
class User:
    id: int
    name: str
    email: str

# Définition du type Order
@strawberry.type
class Order:
    order_id: int
    user_id: int
    status: str

    @strawberry.field
    def user(self) -> User:
        return User(**users_db[self.user_id])

# Définition des requêtes
@strawberry.type
class Query:
    @strawberry.field
    def get_order(self, order_id: int) -> Order:
        order = orders_db.get(order_id)
        if order:
            return Order(**order)
        return None

# Création du schéma GraphQL
schema = strawberry.Schema(query=Query)

# Configuration de l'application FastAPI
app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003)