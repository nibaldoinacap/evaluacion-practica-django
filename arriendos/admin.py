from django.contrib import admin

from .models import Arriendo, Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo', 'valor_diario')
    list_filter = ('marca',)
    search_fields = ('nombre', 'marca', 'modelo')


@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'equipo',
        'fecha_inicio',
        'fecha_termino',
        'valor',
    )
    list_filter = ('fecha_inicio', 'fecha_termino')
    search_fields = ('cliente', 'equipo__nombre')
