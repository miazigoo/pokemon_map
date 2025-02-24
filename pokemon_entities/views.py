import folium
import json

from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, get_list_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    time_now = localtime()
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    pokemon_entitys = get_list_or_404(PokemonEntity,
                                      appeared_at__lte=time_now, disappeared_at__gt=time_now)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url),
        )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, pk=pokemon_id)
    previous_evolution = None
    next_evolution = None
    if pokemon.previous_evolution:
        previous_evolution = {
            'title': pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.pk,
            "img_url": request.build_absolute_uri(pokemon.previous_evolution.photo.url)
        }
    if pokemon.next_evolutions.all():
        evolutions = pokemon.next_evolutions.all().first()
        print('evolutions ', evolutions)
        next_evolution = {
            'title': evolutions.title,
            "pokemon_id": evolutions.pk,
            "img_url": request.build_absolute_uri(evolutions.photo.url)
        }
    pokemon_on_page = {
        'img_url': request.build_absolute_uri(pokemon.photo.url),
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }
    time_now = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = pokemon.pokemon_entity.filter(appeared_at__lte=time_now, disappeared_at__gt=time_now)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.photo.url),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_on_page
    })
