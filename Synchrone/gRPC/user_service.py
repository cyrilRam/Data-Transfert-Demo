import grpc
from concurrent import futures
import user_pb2
import user_pb2_grpc

# Base d'utilisateurs fictive
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"}
}

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        user = users_db.get(request.user_id)
        if user:
            return user_pb2.UserResponse(id=user["id"], name=user["name"], email=user["email"])
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Utilisateur non trouvé")
        return user_pb2.UserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("UserService gRPC démarré sur le port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
