from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from . import models
# Create your views here.

class PlayerListView(ListView):
    template_name = "tenis_chile/players_list.html"
    model = models.Player
    context_object_name = 'players'

    def get_queryset(self):
          return models.Player.objects.filter(nationality='Chile')

class PlayerDetailView(DetailView):
    template_name = "tenis_chile/player_detail.html"
    model = models.Player
    context_object_name = 'player'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = models.Player.objects.get(slug=self.kwargs['slug'])
        context['ranking_history'] = player.rankings.all().order_by('-date')
        context['matches'] = models.TournamentMatch.objects.filter(players__id__exact=player.id).order_by('-date')
        return context
    

class IndexView(TemplateView):
    template_name = "tenis_chile/index.html"

class TournamentDetail(DetailView):
    template_name = "tenis_chile/tournament_detail.html"
    model = models.Tournament
    context_object_name = 'tournament'

class TournamentMatchDetail(DetailView):
    template_name = "tenis_chile/tournament_match_detail.html"
    model = models.TournamentMatch
    context_object_name = 'match'