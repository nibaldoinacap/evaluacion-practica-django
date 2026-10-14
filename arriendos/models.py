from django.db import models


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    valor_diario = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{self.nombre} - {self.marca} {self.modelo}'


class Arriendo(models.Model):
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='arriendos',
    )
    cliente = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_termino = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f'{self.cliente} - {self.equipo.nombre}'
