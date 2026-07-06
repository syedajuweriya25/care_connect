from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .models import User
from .permissions import IsAdmin, IsGuardian, IsResident, IsSecurity, IsVolunteer
from .serializers import LoginSerializer, RegisterSerializer, TokenObtainSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token_serializer = TokenObtainSerializer(data={'email': user.email, 'password': request.data['password']})
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token_serializer = TokenObtainSerializer(data={'email': user.email, 'password': request.data['password']})
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Logged out successfully.'}, status=status.HTTP_200_OK)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.is_verified = True
        request.user.save(update_fields=['is_verified'])
        return Response({'detail': 'Email verification stub completed.', 'is_verified': True}, status=status.HTTP_200_OK)
