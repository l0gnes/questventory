from django.contrib import admin
from .models import Console, Genre, Developer, GameConsoleStock, Game

admin.site.register(Console)
admin.site.register(Genre)
admin.site.register(Developer)
admin.site.register(GameConsoleStock)
admin.site.register(Game)