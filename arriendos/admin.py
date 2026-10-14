from django.contrib import admin

from .models import Arriendo, Equipo


def formato_pesos(valor):
    return f'${int(valor):,}'.replace(',', '.')


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo', 'valor_diario_pesos')
    list_filter = ('marca',)
    search_fields = ('nombre', 'marca', 'modelo')

    @admin.display(description='Valor diario')
    def valor_diario_pesos(self, obj):
        return formato_pesos(obj.valor_diario)


@admin.register(Arriendo)
class ArriendoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'equipo',
        'fecha_inicio',
        'fecha_termino',
        'valor_pesos',
    )
    list_filter = ('fecha_inicio', 'fecha_termino')
    search_fields = ('cliente', 'equipo__nombre')

    @admin.display(description='Valor')
    def valor_pesos(self, obj):
        return formato_pesos(obj.valor)
