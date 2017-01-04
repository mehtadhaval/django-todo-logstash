# Create your views here.
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.serializers import UserRegistrationSerializer, UserSerializer, UserAuthenticationSerializer


class UserActionsViewSet(viewsets.ViewSet):
    queryset = User.objects.all()

    def _create_user_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data
        user_data['token'] = token.key
        return user_data

    @list_route(methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self._create_user_token(user))

    @list_route(methods=['post'])
    def login(self, request):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response(self._create_user_token(user))

    @list_route(methods=['post'], permission_classes=(IsAuthenticated, ))
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response()
