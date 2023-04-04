from django.contrib import admin
from .models import Pokemon, PokemonEntity

class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ['lat', 'lon', 'pokemon']

admin.site.register(PokemonEntity,PokemonEntityAdmin)

admin.site.register(Pokemon)