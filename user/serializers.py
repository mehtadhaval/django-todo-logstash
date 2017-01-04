from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'username', 'password')

    def save(self, **kwargs):
        return User.objects.create_user(**self.validated_data)


class UserAuthenticationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        _('Your user rights have been revoked as your account has been deactivated. '
                          'Please contact your admin for more details.')
                    )

            else:
                raise serializers.ValidationError(_('Invalid Credentials. Please Try Again!'))
        else:
            msg = _('Please provide credentials.')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')
