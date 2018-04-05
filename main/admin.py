from django.contrib import admin
from main.models import Pie, Game

class PieAdmin(admin.ModelAdmin):
    fields = ['text', 'owner', 'date_added']
    list_display = ('text', 'owner', 'date_added')
    list_filter = ['date_added']
    date_hierarchy = 'date_added'
    ordering = ['-date_added']

admin.site.register(Pie, PieAdmin)
admin.site.register(Game)
