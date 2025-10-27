
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class Evento(models.Model):

    titulo = models.CharField(max_length=200)
    fecha_hora = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    plazas_disponibles = models.PositiveIntegerField(default=20)
    

    descripcion = models.TextField(null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscritos')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f'{self.usuario.username} -> {self.evento.titulo}'