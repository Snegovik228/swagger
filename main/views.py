from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate, login



@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirmPassword')

    if password != confirm_password:
        return Response({'error': 'Пароли не совпадают'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)

    access = AccessToken.for_user(user)
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Пользователь успешно зарегистрирован!',
        'access_token': str(access),
        'refresh_token': str(refresh)
    }, status=201)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        access = AccessToken.for_user(user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(access),
            'refresh_token': str(refresh)
        }, status=200)
    else:
        return Response({'error': 'Произошла ошибка'}, status=401)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_tokens(request):
    user = request.user
    refresh_token = request.data.get('refresh_token')

    # Проверяем, что пользователь отправляет запрос на обновление своего Refresh Token
    if user.token == refresh_token:
        try:

            token = RefreshToken(refresh_token)

            access_token = token.access_token
            refresh_token = token

            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }, status=200)

        except Exception as e:
            return Response({'error': 'Недействительный Refresh Token'}, status=400)
    else:
        return Response({'error': 'Недостаточно прав для обновления токенов'}, status=403)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user

    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }

    return Response(user_data, status=200)