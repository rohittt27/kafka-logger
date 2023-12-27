
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.kafka_logger import KafkaLogger
from api.models import Item
from api.serializers import ItemSerializer, UserLoginSerializer
from django.contrib.auth import authenticate

# class UserLoginView(APIView):
#     serializer_class = UserLoginSerializer

#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             breakpoint()
#             data = request.data
#             serializer = self.serializer_class(data=data, context={"request": request})

#             if serializer.is_valid():
#                 email = serializer.validated_data.get("email")
#                 password = serializer.validated_data.get("password")

#                 user = authenticate(username=email, password=password)

#                 if user:
#                     # User authentication is successful
#                     log_message = f"User Login Successfully: {serializer.data}"
#                     kafka_logger = KafkaLogger(bootstrap_servers='localhost:9092', topic='logs')
#                     kafka_logger.log_message(log_message)

#                     return Response(
#                         data={
#                             "message": "success",
#                             "status": status.HTTP_200_OK,
#                             "data": serializer.data,
#                             "errors": None,
#                         },
#                         status=status.HTTP_200_OK,
#                     )
#                 else:
#                     # User authentication failed
#                     log_message = f"Login failed: Invalid credentials for {email}"
#                     kafka_logger = KafkaLogger(bootstrap_servers='localhost:9092', topic='logs')
#                     kafka_logger.log_message(log_message)

#                     return Response(
#                         data={
#                             "message": "failed",
#                             "status": status.HTTP_401_UNAUTHORIZED,
#                             "data": None,
#                             "errors": "Invalid credentials",
#                         },
#                         status=status.HTTP_401_UNAUTHORIZED,
#                     )
#             else:
#                 log_message = f"Login failed: Invalid serializer data - {serializer.errors}"
#                 kafka_logger = KafkaLogger(bootstrap_servers='localhost:9092', topic='logs')
#                 kafka_logger.log_message(log_message)

#                 return Response(
#                     data={
#                         "message": "failed",
#                         "status": status.HTTP_400_BAD_REQUEST,
#                         "data": None,
#                         "errors": serializer.errors,
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         except Exception as e:
#             log_message = f"Internal Server Error: {str(e)}"
#             kafka_logger = KafkaLogger(bootstrap_servers='localhost:9092', topic='logs')
#             kafka_logger.log_message(log_message)

#             return Response(
#                 data={
#                     "message": "Internal Server Error",
#                     "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     "data": None,
#                     "errors": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        log_message = f"Item created: {serializer.data}"
        kafka_logger = KafkaLogger(bootstrap_servers='kafka:9092', topic='logs')
        kafka_logger.log_message(log_message)

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    # permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()
        log_message = f"Item updated: {serializer.data}"
        kafka_logger = KafkaLogger(bootstrap_servers='kafka:9092', topic='logs')
        kafka_logger.log_message(log_message)

    def perform_destroy(self, instance):
        log_message = f"Item deleted: {instance}"
        kafka_logger = KafkaLogger(bootstrap_servers='kafka:9092', topic='logs')
        kafka_logger.log_message(log_message)
        instance.delete()