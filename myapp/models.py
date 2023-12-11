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

    def get_player_names(self):
        return ", ".join([f"{player.first_name} {player.family_name} ({player.player_number})" for player in self.players.all()])

    def player_count(self):
        return self.players.count()

class Player(models.Model):
    name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    player_number = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.family_name} ({self.team.name}) - {self.player_number}"

class Match(models.Model):
    STATUS_CHOICES = [
        ('À venir', 'À venir'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
    ]
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    match_time = models.DateTimeField()
    venue = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='À venir')
    score_team1 = models.IntegerField(null=True, blank=True)
    score_team2 = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)  # Actual start time of the match
    end_time = models.DateTimeField(null=True, blank=True)  # Actual end time of the match
    odds_team1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Odds for team 1
    odds_team2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Odds for team 2


    def __str__(self):
        return f"{self.team1.name} vs {self.team2.name} - {self.match_time}"

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.match_time + timedelta(hours=1)
        super().save(*args, **kwargs)

class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    chosen_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_placed = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return f"Bet by {self.user.username} on {self.match}"


