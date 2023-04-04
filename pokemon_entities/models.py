from django.db import models  # noqa F401
from django.utils.safestring import mark_safe


class Pokemon(models.Model):
    title = models.CharField(verbose_name="Покемон_ru", max_length=200)
    title_en = models.CharField(verbose_name="Покемон_en", max_length=200, null=True)
    title_jp = models.CharField(verbose_name="Покемон_jp", max_length=200, null=True)
    photo = models.ImageField(verbose_name="Картинка", upload_to='pokemons', null=True)
    description = models.TextField(verbose_name='Описание', null=True)
    previous_evolution = models.ForeignKey("Pokemon", on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name="Эволюция из кого", related_name='evolution_from')
    next_evolution = models.ForeignKey("Pokemon", on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name="Эволюция в кого", related_name='evolution_in')

    def __str__(self):
        return self.title

    @property
    def photo_preview(self):
        if self.photo:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.photo.url))
        return ""


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон")
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField(verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Появится в:")
    disappeared_at = models.DateTimeField(verbose_name="Исчезнет в:")
    level = models.IntegerField(verbose_name="Уровень:", null=True)
    health = models.IntegerField(verbose_name="Здоровье:", null=True)
    strength = models.IntegerField(verbose_name="Атака:", null=True)
    defense = models.IntegerField(verbose_name="Защита:", null=True)
    stamina = models.IntegerField(verbose_name="Выносливость:", null=True)
