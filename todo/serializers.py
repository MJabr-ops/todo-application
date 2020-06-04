from rest_framework import serializers
from .models import Karbar,todo,TodoBasket
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

class KarbarSerializer(serializers.Serializer):
    first_name=serializers.CharField(max_length=50)
    last_name=serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField(max_length=50)
    tokens = serializers.SerializerMethodField()
    def create(self, validated_data):

        return Karbar.objects.create(**validated_data)

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data


    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)
    def validate_first_name(self,first_name):
        first_name=first_name.lower()
        if "ghazanfar" in first_name.lower():
            raise  serializers.ValidationError("god damn you ghazanfar what the hell are you doing here?")
        return first_name

    def validate(self, attrs):
        email=attrs['email']
        if Karbar.objects.filter(email=email).exists():
            raise serializers.ValidationError("email already exists try to login ")
        return attrs
    class Meta:
        model=Karbar
        fields='__all__'
class TodoBasketSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        print(validated_data)

        return TodoBasket.objects.create(**validated_data)

    class Meta:

        model=TodoBasket

        fields='__all__'


class TodoSerializer(serializers.ModelSerializer):


    class Meta:
        model=todo
        fields='__all__'




