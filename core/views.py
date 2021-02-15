import os

from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Balance, Round, Game
from .serializers import UserSerializer, RoundSerializer, BalanceSerializer, GameSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user = serializer.instance
        finally:
            token, created = Token.objects.get_or_create(user=user)
            user.balance, created = Balance.objects.get_or_create(user=user)
            return Response({'id': user.id,
                             'username': user.username,
                             'email': user.email,
                             'balance': BalanceSerializer(user.balance).data,
                             'token': token.key})


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=True, methods=['get'])
    def get_balance(self, request, pk=None):
        return Response(BalanceSerializer(Balance.objects.get(user_id=pk)).data)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'])
    def games(self, request, pk=None):
        return Response(GameSerializer(Game.objects.filter(user_id=pk), many=True).data)

    @action(detail=True, methods=['get'])
    def get_game(self, request, pk=None, pk_game=None):
        return Response(GameSerializer(Game.objects.get(user_id=pk, pk=pk_game)).data)

    @action(detail=True, methods=['post'])
    def start_game(self, request, pk=None):
        game = Game.objects.create(user_id=pk)
        game.save()
        return Response(GameSerializer(game).data)


class RoundViewSet(viewsets.ModelViewSet):
    queryset = Round.objects.all()
    serializer_class = RoundSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['get'])
    def rounds(self, request, pk=None, pk_game=None):
        return Response(RoundSerializer(Round.objects.filter(game=Game.objects.get(pk=pk_game))).data)

    @action(detail=True, methods=['get'])
    def get_round(self, request, pk=None, pk_game=None, pk_round=None):
        return Response(RoundSerializer(Round.objects.filter(
            game=Game.objects.get(pk=pk_game), pk=pk_round), many=True).data)

    @action(detail=True, methods=['post'])
    def start_round(self, request, pk=None, pk_game=None):
        game = Game.objects.get(user_id=pk, pk=pk_game)
        result = round(int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1))
        game_round = Round.objects.create(game=game,
                                          bet=int(request.POST['bet']),
                                          choice=request.POST['choice'],
                                          result=result)
        game_round.save()
        user = User.objects.get(pk=pk)
        balance = Balance.objects.get(user=user)
        balance.last_balance = balance.balance
        if int(game_round.result) == int(game_round.choice):
            game.bank = int(game.bank) + int(game_round.bet)
            balance.new_balance = balance.new_balance + int(game_round.bet)
        else:
            game.bank = int(game.bank) - int(game_round.bet)
            balance.new_balance = int(balance.new_balance) - int(game_round.bet)
        balance.balance = balance.new_balance
        balance.save()
        game.save()
        rounds = Round.objects.filter(game=game)
        if rounds.count() == 5:
            if game.bank >= 0:
                game.result = 1
            else:
                game.result = 0
            game.save()
            return Response({'id': user.id,
                             'username': user.username,
                             'email': user.email,
                             'balance': BalanceSerializer(balance).data,
                             'game': GameSerializer(game).data,
                             'round': RoundSerializer(game_round).data})
        return Response(RoundSerializer(game_round).data)
