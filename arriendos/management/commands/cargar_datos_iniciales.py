from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from arriendos.models import Arriendo, Equipo


class Command(BaseCommand):
    help = 'Carga grupos, usuarios y registros iniciales del sistema.'

    def handle(self, *args, **options):
        permisos = Permission.objects.filter(
            content_type__app_label='arriendos',
            content_type__model__in=('equipo', 'arriendo'),
            codename__in=('view_equipo', 'add_equipo', 'change_equipo',
                          'view_arriendo', 'add_arriendo', 'change_arriendo'),
        )
        vendedor, _ = Group.objects.get_or_create(name='Vendedor')
        vendedor.permissions.set(permisos)

        supervisor, _ = Group.objects.get_or_create(name='Supervisor')
        supervisor.permissions.set(
            permisos.filter(codename__startswith='view_')
        )

        user_model = get_user_model()
        vendedor_user, _ = user_model.objects.get_or_create(username='vendedor')
        vendedor_user.set_password('Inacap.2026')
        vendedor_user.is_staff = True
        vendedor_user.is_superuser = False
        vendedor_user.save()
        vendedor_user.groups.set([vendedor])

        supervisor_user, _ = user_model.objects.get_or_create(username='supervisor')
        supervisor_user.set_password('Inacap.2026')
        supervisor_user.is_staff = True
        supervisor_user.is_superuser = False
        supervisor_user.save()
        supervisor_user.groups.set([supervisor])

        equipos = [
            ('Cámara profesional', 'Canon', 'EOS R6', 45000),
            ('Proyector multimedia', 'Epson', 'PowerLite X49', 30000),
            ('Notebook', 'Lenovo', 'ThinkPad E14', 25000),
        ]
        equipos_creados = []
        for nombre, marca, modelo, valor_diario in equipos:
            equipo, _ = Equipo.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'marca': marca,
                    'modelo': modelo,
                    'valor_diario': valor_diario,
                },
            )
            equipos_creados.append(equipo)

        arriendos = [
            ('Ana Pérez', equipos_creados[0], date(2026, 10, 1),
             date(2026, 10, 3), 90000),
            ('Bruno Soto', equipos_creados[0], date(2026, 10, 5),
             date(2026, 10, 6), 45000),
            ('Carla Díaz', equipos_creados[1], date(2026, 10, 2),
             date(2026, 10, 4), 60000),
            ('Diego Rojas', equipos_creados[1], date(2026, 10, 8),
             date(2026, 10, 9), 30000),
            ('Elena Muñoz', equipos_creados[2], date(2026, 10, 10),
             date(2026, 10, 12), 75000),
            ('Felipe Vargas', equipos_creados[2], date(2026, 10, 15),
             date(2026, 10, 16), 50000),
        ]
        for cliente, equipo, inicio, termino, valor in arriendos:
            Arriendo.objects.update_or_create(
                cliente=cliente,
                equipo=equipo,
                fecha_inicio=inicio,
                defaults={
                    'fecha_termino': termino,
                    'valor': valor,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            'Grupos, usuarios, equipos y arriendos cargados correctamente.'
        ))
