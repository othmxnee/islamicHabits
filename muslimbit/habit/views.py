from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Create or retrieve token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to log the user out
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)  