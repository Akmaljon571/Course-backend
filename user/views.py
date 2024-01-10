from django.contrib.auth.hashers import check_password
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken

from .serializers import *
from .utils import send_email
from .models import CustomUser


class RegistrationView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(data={'message': "BAD REQUEST", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            oldUser = CustomUser.objects.get(email=email)
            if oldUser:
                return Response(data={'message': "User already exists", "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            random = send_email(email)

            cache.set(random, {"email": email, "password": password, 'status': False})
            return Response(data={'message': "Send Email code", "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)


class RegisterCodeView(CreateAPIView):
    serializer_class = RegistrationCodeSerializer

    def create(self, request, **kwargs):
        code = request.data.get('code')
        data = cache.get(code)

        if not data:
            return Response(data={'message': 'Code Invalid', "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        cache.delete(code)
        cache.set(code, {"email": data['email'], "password": data['password'], 'status': True})
        return Response(data={"status": status.HTTP_200_OK, "code": code},
                        status=status.HTTP_200_OK)


class RegisterCreateView(CreateAPIView):
    serializer_class = RegistrationSchemaCreateSerializer
    parser_classes = (MultiPartParser,)

    def create(self, request, **kwargs):
        code = request.data.get('code')
        cache_data = cache.get(code)
        if not cache_data:
            return Response(data={'message': 'Code Invalid', "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        data = {
            "email": cache_data['email'],
            "username": request.data.get('username'),
            "password": cache_data['password'],
            "age": request.data.get('age'),
            "region": request.data.get('region'),
            "phone": request.data.get('phone'),
            "avatar": request.data.get('avatar')
        }
        serializer = RegistrationCreateSerializer(data=data)
        if not serializer.is_valid():
            cache.delete(code)
            return Response(data={'message': serializer.errors, 'status': status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        cache.delete(code)
        return Response(response_data, status=status.HTTP_201_CREATED)


class PasswordEmailView(CreateAPIView):
    serializer_class = PasswordEmailSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        random = send_email(email)

        cache.set(random, {"email": email})
        return Response(data={'message': "Send Email code", "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class PasswordCodeView(CreateAPIView):
    serializer_class = PasswordCodeSerializer

    def create(self, request, **kwargs):
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        data = cache.get(code)
        if not data or not new_password:
            return Response(data={'message': 'Code Invalid', "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.get(email=data['email'])
            user.set_password(new_password)
            user.save()
        except:
            cache.delete(code)
            return Response(data={'message': 'Code Invalid2', "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
        cache.delete(code)
        return Response(data={'message': 'Password updated successfully', "status": status.HTTP_200_OK},
                        status=status.HTTP_200_OK)


class LoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = CustomUser.objects.filter(Q(email=email)).first()
            if user and check_password(password, user.password):
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)

            return Response(data={'error': 'Invalid credentials', "status": status.HTTP_401_UNAUTHORIZED},
                            status=status.HTTP_401_UNAUTHORIZED)


class TokenRefreshView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(data={'error': 'Refresh token is required', "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            refresh.verify()
        except TokenError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(refresh.access_token, AccessToken):
            return Response({'error': 'Token has wrong type'}, status=status.HTTP_400_BAD_REQUEST)

        new_access_token = str(refresh.access_token)
        return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)


class UserProfileDetail(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
