from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



class Team(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='team_logos', blank=True, null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    coach_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    # Vous pouvez ajouter d'autres champs ici, par exemple numéro, position, etc.

    def __str__(self):
        return f"{self.name} ({self.team.name})"

class Match(models.Model):
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    match_time = models.DateTimeField()
    venue = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, default='Upcoming')  # Exemples: 'À venir', 'En cours', 'Terminé'
    score_team1 = models.IntegerField(null=True, blank=True)
    score_team2 = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.match_time}"

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    chosen_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_placed = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Bet by {self.user.username} on {self.match}"


