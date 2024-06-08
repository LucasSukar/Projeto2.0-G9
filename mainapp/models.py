from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
    
class Categoria(models.Model):
    tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipo

class Cafe(models.Model):
    
    AVALIACAO_CHOICES = [
        (0, '0 Estrelas'),
        (1, '1 Estrela'),
        (2, '2 Estrelas'),
        (3, '3 Estrelas'),
        (4, '4 Estrelas'),
        (5, '5 Estrelas'),
    ]
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    cntt = models.CharField(max_length=15)
    tipo=models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    avaliacao=models.IntegerField(choices=AVALIACAO_CHOICES, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cafes')
    isbn = models.CharField(max_length=13, null=True)
    in_collection = models.BooleanField(default=True)
    is_frequente = models.BooleanField(default=False)
    is_favorita = models.BooleanField(default=False)
    is_wish = models.BooleanField(default=False)
    caracteristicas = models.TextField(blank=True)


    def get_caracteristicas_list(self):
        return self.caracteristicas.split(",")

    def set_caracteristicas_list(self, caracteristicas_list):
        self.caracteristicas = ",".join(caracteristicas_list)

    caracteristicas_list = property(get_caracteristicas_list, set_caracteristicas_list)

    def __str__(self):
        return self.nome

class Comentario(models.Model):
    endereco = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='comentarios') 

    def __str__(self):
        return f"Comentário de {self.endereco} em {self.cafe}: {self.texto}"

class Novidade(models.Model):
    endereco = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='novidade') 

    def __str__(self):
        return f"Novidade de {self.endereco} em {self.cafe}: {self.texto}"