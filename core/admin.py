from django.contrib import admin

from .models import Balance, Game, Round


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    pass


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    pass
