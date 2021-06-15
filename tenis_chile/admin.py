from django.contrib import admin
from django.contrib.admin.decorators import register
from . import models

# Register your models here.
class PlayerAdmin(admin.ModelAdmin): # name can be anything
    prepopulated_fields = {"slug": ("first_name","last_name",)}
    # list_filter
    # list_display

class RankingHistoryAdmin(admin.ModelAdmin): # name can be anything
    list_filter = ["player"]
    list_display = ["player", "date", "ranking"]

class TournamentMatchAdmin(admin.ModelAdmin): # name can be anything
    list_filter = ["tournament__name", "tournament__date", "winners"]
    list_display = ["tournament", "date", "get_winners"]

class TournamentAdmin(admin.ModelAdmin): # name can be anything
    list_filter = ["tournament_type", "date", "surface"]

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.RankingHistory, RankingHistoryAdmin)
admin.site.register(models.Tournament, TournamentAdmin)
admin.site.register(models.TournamentMatch, TournamentMatchAdmin)
admin.site.register(models.TournamentType)
