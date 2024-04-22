from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class Categoria(models.Model):
    genero = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.genero

class Cafe(models.Model):
    STATUS_LEITURA_CHOICES = [
        ('NL', 'Fui'),
        ('EL', 'Quero ir'),
    ]
    AVALIACAO_CHOICES = [
        (0, '0 Estrelas'),
        (1, '1 Estrela'),
        (2, '2 Estrelas'),
        (3, '3 Estrelas'),
        (4, '4 Estrelas'),
        (5, '5 Estrelas'),
    ]
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    anopublicado = models.IntegerField()
    genero=models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    status_leitura=models.CharField(max_length=2, choices=STATUS_LEITURA_CHOICES, default='NL')
    avaliacao=models.IntegerField(choices=AVALIACAO_CHOICES, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cafes')
    isbn = models.CharField(max_length=13, null=True)
    in_wishlist = models.BooleanField(default=False)
    in_collection = models.BooleanField(default=True)
    def __str__(self):
        return self.titulo
    
class ListaDesejos(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lista_desejos',null=True)
    cafes = models.ManyToManyField('Cafe', related_name='desejado_por')

    def __str__(self):
        return f" Lista de desejos de {self.usuario}"


class BookHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date_started = models.DateField(default=timezone.now)
    date_finished = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.book_title} ({self.author})"
