from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    SendCodeSerializer, RegisterSerializer, LoginSerializer,
    UserProfileSerializer, UserUpdateSerializer,
)
from .utils import send_email_code, send_phone_code


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code(request):
    serializer = SendCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    target = serializer.validated_data['target']
    code_type = serializer.validated_data['code_type']

    if code_type == 'email':
        send_email_code(target)
    else:
        send_phone_code(target)

    return Response({'detail': '验证码已发送'})


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    target = serializer.validated_data['target']
    code_type = serializer.validated_data['code_type']
    if code_type == 'email':
        if User.objects.filter(email=target).exists():
            return Response({'detail': '该邮箱已注册'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if User.objects.filter(phone=target).exists():
            return Response({'detail': '该手机号已注册'}, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserProfileSerializer(user, context={'request': request}).data,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_code(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.validated_data['_user']
    vc = serializer.validated_data['_vc']
    vc.is_used = True
    vc.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserProfileSerializer(user, context={'request': request}).data,
    })


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_serializer_context(self):
        return {'request': self.request}

