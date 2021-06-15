from tenis_chile.views import PlayerListView
from django.urls import path 
from . import views

urlpatterns = [
    path("jugadores/", views.PlayerListView.as_view(), name="players-list"),
    path("jugadores/<slug:slug>", views.PlayerDetailView.as_view(), name="player-detail"),
    path("", views.IndexView.as_view(), name="index"),
    path("torneos/<int:pk>", views.TournamentDetail.as_view(), name="tournament-detail"),
    path("partidos/<int:pk>", views.TournamentMatchDetail.as_view(), name="tournament-match-detail")

]
