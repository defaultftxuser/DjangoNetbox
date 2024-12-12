from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.infra.repos.users.users_repo import UserRepository, TokenRepository
from src.infra.serializers.users.serializers import RegistrationSerializer
from src.infra.services.users.user_service import UserService


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_service = UserService(repository=UserRepository(), token_repository=TokenRepository())
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            token = user_service.create(data=serializer.validated_data)
            return Response({
                "token": token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except AttributeError:
            return Response({"detail": "User is not logged in."}, status=400)

        return Response({"detail": "Successfully logged out."}, status=200)