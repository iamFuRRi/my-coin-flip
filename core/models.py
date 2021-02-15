from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    RESULT_OPTIONS = (
        (0, 'DEFEAT'),
        (1, 'WIN'),
    )

    result = models.IntegerField(choices=RESULT_OPTIONS, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    bank = models.IntegerField(default=0)

    def user_name(self):
        return self.user.username

    def __str__(self):
        return "Username: {0} - Result: {1} - Bank: {2}".format(self.user_name(), self.RESULT_OPTIONS[self.result][1],
                                                                self.bank)


class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)

    COIN_OPTIONS = (
        (0, 'HEAD'),
        (1, 'TAIL'),
    )

    RESULT_OPTIONS = (
        (0, 'DEFEAT'),
        (1, 'WIN'),
    )

    bet = models.IntegerField(default=0)
    choice = models.IntegerField(choices=COIN_OPTIONS)
    result = models.IntegerField(choices=RESULT_OPTIONS)

    def __str__(self):
        return "Game ID: {0} - Bet: {1} - Choice: {2} - Result: {3}".format(
            self.game.id, self.bet, self.COIN_OPTIONS[self.choice][1],
            self.RESULT_OPTIONS[self.result][1]
        )


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    balance = models.IntegerField(default=50)
    last_balance = models.IntegerField(default=50)
    new_balance = models.IntegerField(default=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def user_name(self):
        return self.user.username

    def __str__(self):
        return "Username: {0} - Balance: {1}".format(self.user_name(), self.balance)
