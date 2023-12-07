from django.contrib import admin
from .models import Team, Player, Match, Bet


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'coach_name')
    search_fields = ('name', 'coach_name')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team')
    list_filter = ('team',)
    search_fields = ('name',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('team1', 'team2', 'match_time', 'status')
    list_filter = ('status', 'match_time')
    search_fields = ('team1__name', 'team2__name')


class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'amount', 'is_winner')
    list_filter = ('is_winner',)
    search_fields = ('user__username', 'match__team1__name', 'match__team2__name')


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Bet, BetAdmin)
