from django.db import models  # noqa F401
from django.utils.safestring import mark_safe


class Pokemon(models.Model):
    title = models.CharField(verbose_name="Покемон_ru", max_length=200)
    title_en = models.CharField(verbose_name="Покемон_en", max_length=200, blank=True)
    title_jp = models.CharField(verbose_name="Покемон_jp", max_length=200, blank=True)
    photo = models.ImageField(verbose_name="Картинка", upload_to='pokemons', blank=True)
    description = models.TextField(verbose_name='Описание')
    previous_evolution = models.ForeignKey("Pokemon", on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Из кого эволюционирует", related_name='next_evolutions')

    def __str__(self):
        return self.title

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.photo.url))
        return ""


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE,
                                verbose_name="Покемон", related_name='pokemon_entitys')
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появится в:", blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет в:", blank=True)
    level = models.IntegerField(verbose_name="Уровень:")
    health = models.IntegerField(verbose_name="Здоровье:")
    strength = models.IntegerField(verbose_name="Атака:")
    defense = models.IntegerField(verbose_name="Защита:")
    stamina = models.IntegerField(verbose_name="Выносливость:")

    def __str__(self):
        return self.pokemon.title
