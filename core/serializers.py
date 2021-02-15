from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Balance, Game, Round


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'balance', 'last_balance', 'new_balance']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'result', 'bank']


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ['auth_token']


class UserSerializer(serializers.ModelSerializer):
    # auth_token = TokenSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # , 'auth_token']
        extra_kwargs = {'password': {'write_only': True}}

    # def create(self, validated_data):
    #    instance = User(
    #        username=validated_data['username'],
    #        email=validated_data['email'],
    #    )
    #    instance.set_password(validated_data['password'])
    #    instance.save()
    #    instance.balance = Balance.objects.create(user=instance)
    #    return instance


class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = ['id', 'bet', 'choice', 'result']
