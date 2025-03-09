import grpc
import user_pb2
import user_pb2_grpc
from concurrent import futures

class OrderService:
    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = user_pb2_grpc.UserServiceStub(self.channel)

    def get_order(self, user_id):
        try:
            request = user_pb2.UserRequest(user_id=user_id)
            user_data = self.stub.GetUser(request)
            return {
                "order_id": 101,
                "user": {
                    "id": user_data.id,
                    "name": user_data.name,
                    "email": user_data.email
                },
                "status": "En cours"
            }
        except grpc.RpcError as e:
            return {"error": "Utilisateur non trouvé"}, 404

def serve():
    order_service = OrderService()
    print(order_service.get_order(1))  # Test avec un ID utilisateur existant
    print(order_service.get_order(3))  # Test avec un ID inexistant

if __name__ == "__main__":
    serve()
