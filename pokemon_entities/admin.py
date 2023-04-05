from django.contrib import admin
from .models import Pokemon, PokemonEntity

class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ['pokemon']

admin.site.register(PokemonEntity,PokemonEntityAdmin)


class PokemonAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo']
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        return obj.photo_preview

    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True

admin.site.register(Pokemon, PokemonAdmin)