from django.db import models
from django.core.validators import MinValueValidator
from django_resized import ResizedImageField
import re
from datetime import date


class Player(models.Model):
    FOREHAND_1 = 'RF'
    FOREHAND_2 = 'LF'
    U_FOREHAND = 'UF'
    BACKHAND_1 = 'R2'
    BACKHAND_2 = 'R1'
    U_BACKHAND = 'UB'
    FOREHAND_CHOICES = [
        (FOREHAND_1, 'Diestro'),
        (FOREHAND_2, 'Zurdo'),
        (U_FOREHAND, 'Desconocido'),
    ]
    BACKHAND_CHOICES = [
        (BACKHAND_1, 'Revés a dos manos'),
        (BACKHAND_2, 'Revés a una mano'),
        (U_BACKHAND, 'Desconocido'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = ResizedImageField(size=[200, 200], upload_to='uploads', null=True)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50, default='Chile')
    weight = models.IntegerField(blank=True, null=True)  # in kg
    height = models.IntegerField(blank=True, null=True)  # in cm
    # blank allow empty strings in form
    coach = models.CharField(max_length=100, blank=True)
    birth_place = models.CharField(max_length=50, blank=True)
    residence = models.CharField(max_length=50, blank=True)
    actual_ranking = models.IntegerField(
        null=True, validators=[MinValueValidator(0)])
    pro_titles = models.IntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)])
    bio = models.TextField(blank=True)
    sponsor = models.CharField(blank=True, max_length=50)
    racket = models.CharField(blank=True, max_length=50)
    actual_points = models.IntegerField(
        null=True, validators=[MinValueValidator(0)])
    forehand = models.CharField(
        blank=True, max_length=2, choices=FOREHAND_CHOICES)
    backhand = models.CharField(
        blank=True, max_length=2, choices=BACKHAND_CHOICES)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_age(self):
        today = date.today()
        born = self.birth_date
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class RankingHistory(models.Model):
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='rankings')
    date = models.DateField()
    ranking = models.IntegerField(validators=[MinValueValidator(0)])
    points = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)])


class TournamentType(models.Model):
    name = models.CharField(max_length=50)
    image = ResizedImageField(
        size=[200, 200], upload_to='uploads/tournament_types', null=True)
    level = models.CharField(max_length=50)
    points = models.IntegerField(validators=[MinValueValidator(0)])
    association = models.CharField(max_length=50)
    # prize = models.IntegerField(validators=[MinValueValidator(0)]) # dollars

    def __str__(self):
        return self.name


class Tournament(models.Model):
    CLAY = 'C'
    HARD = 'H'
    GRASS = 'G'
    CARPET = 'P'
    SURFACE_CHOICES = [
        (CLAY, 'Arcilla'),
        (HARD, 'Cancha rápida'),
        (GRASS, 'Pasto'),
        (CARPET, 'Carpeta')
    ]
    name = models.CharField(max_length=50)
    image = ResizedImageField(
        size=[200, 200], upload_to='uploads/tournaments', null=True)
    date = models.DateField()
    surface = models.CharField(max_length=1, choices=SURFACE_CHOICES)
    players = models.ManyToManyField(Player, related_name='tournaments')
    tournament_type = models.OneToOneField(
        TournamentType, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    rounds = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    prize = models.IntegerField(null=True, validators=[
                                MinValueValidator(0)])  # dollars

    def __str__(self):
        return self.name


class TournamentMatch(models.Model):
    LOCAL = '1'
    AWAY = '2'
    NOT_PLAYED = 'X'
    WINNER_CHOICES = [
        (LOCAL, 'Dupla 1'),
        (AWAY, 'Dupla 2'),
        (NOT_PLAYED, 'No jugado'),
    ]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player, null=True, related_name='+')
    date = models.DateField()
    isLive = models.BooleanField()
    set_1 = models.CharField(max_length=8)
    set_2 = models.CharField(max_length=8)
    set_3 = models.CharField(max_length=8, blank=True)
    set_4 = models.CharField(max_length=8, blank=True)
    set_5 = models.CharField(max_length=8, blank=True)
    winners = models.ManyToManyField(
        Player, blank=True, null=True, related_name='+')
    round_number = models.IntegerField(validators=[MinValueValidator(1)])
    highlights_embed = models.CharField(max_length=300, blank=True, null=True)
    streaming_embed = models.TextField(blank=True, null=True)

    def get_winners(self):
        winners = self.winners.all()
        lst = []
        for winner in winners:
            lst.append(winner.get_full_name())
        return ' - '.join(lst)
