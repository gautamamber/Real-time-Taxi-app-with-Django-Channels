from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer
    """
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2', 'first_name', 'last_name'
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        """
        Match password1 and password2
        :param attrs:
        :return:
        """
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Password do not match")
        return attrs

    def create(self, validated_data):
        """
        Create user
        :param validated_data:
        :return:
        """
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)


class LoginSerializer(TokenObtainPairSerializer):
    """
    Login serializer
     LogInSerializer that serializes the User object and adds the data to the token payload as private claims.
     (We avoid overwriting the id claim, since the token already includes it by
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token['key'] = value
        return token


class TripSerializer(serializers.ModelSerializer):
    """
    Trip serializer
    """

    class Meta:
        model = models.Trip
        fields = "__all__"
        read_only_fields = ('id', 'created', 'updated',)


class NestedTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Trip
        fields = '__all__'
        depth = 1