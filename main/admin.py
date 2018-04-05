from django.contrib import admin
from main.models import Pie, Game

class PieAdmin(admin.ModelAdmin):
    fields = ['text', 'owner', 'date_added']
    list_display = ('text', 'owner', 'date_added')
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    ordering = ['-date_added']

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'system', 'owner', 'date_added', 'is_displayed')
    list_filter = ['date_added', 'owner']
    date_hierarchy = 'date_added'
    ordering = ['-date_added']
    search_fields = ['title', 'gamemaster', 'system', 'description']

admin.site.register(Pie, PieAdmin)
admin.site.register(Game, GameAdmin)
