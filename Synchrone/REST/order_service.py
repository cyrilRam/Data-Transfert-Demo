import requests
from fastapi import FastAPI

app = FastAPI()

USER_SERVICE_URL = "http://127.0.0.1:8001/users/"


@app.get("/orders/{user_id}")
def get_order(user_id: int):
    response = requests.get(f"{USER_SERVICE_URL}{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        return {
            "order_id": 101,
            "user": user_data,
            "status": "En cours"
        }
    return {"error": "Utilisateur non trouvé"}, 404


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
