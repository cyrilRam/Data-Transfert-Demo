from fastapi import FastAPI

app = FastAPI()

# Base d'utilisateurs fictive
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user:
        return user
    return {"error": "Utilisateur non trouvé"}, 404

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
