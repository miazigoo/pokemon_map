from django.db import models  # noqa F401
from django.utils.safestring import mark_safe


class Pokemon (models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='pokemons', null=True)

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
