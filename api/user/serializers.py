"""serializers for user"""
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer dla user"""
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create user"""

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Updating user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type', 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validating"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            password=password,
            username=email,
            request=self.context.get('request'),

        )

        if not user:
            msg = _('Unable to authenticate')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
