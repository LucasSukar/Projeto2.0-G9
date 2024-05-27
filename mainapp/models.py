from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
    
class Categoria(models.Model):
    tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipo

class Cafe(models.Model):
    STATUS_CAFETERIA_CHOICES = [
        ('NL', 'Não Favorita'),
        ('EL', 'Favorita'),
    ]
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
    status_cafeteria=models.CharField(max_length=2, choices=STATUS_CAFETERIA_CHOICES, default='NL')
    avaliacao=models.IntegerField(choices=AVALIACAO_CHOICES, default=0)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cafes')
    isbn = models.CharField(max_length=13, null=True)
    in_wishlist = models.BooleanField(default=False)
    in_collection = models.BooleanField(default=True)
    avaliacao = models.IntegerField(choices=AVALIACAO_CHOICES, null=True, blank=True)
    is_frequente = models.BooleanField(default=False)
    caracteristicas = models.TextField(blank=True)

    #adicionando o adicionar caracteristicas da cafeteria feito por lunna e seu amigo
    def get_caracteristicas_list(self):
        return self.caracteristicas.split(",")  # Ou outro delimitador, dependendo de como você os separou

    def set_caracteristicas_list(self, caracteristicas_list):
        self.caracteristicas = ",".join(caracteristicas_list)

    caracteristicas_list = property(get_caracteristicas_list, set_caracteristicas_list)

    def __str__(self):
        return self.nome
    
class ListaDesejos(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lista_desejos',null=True)
    cafes = models.ManyToManyField('Cafe', related_name='desejado_por')

    def __str__(self):
        return f" Lista de desejos de {self.usuario}"
    
    def comentarios(self):
        return Comentario.objects.filter(cafe=self)


class CoffeeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coffee_title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date_started = models.DateField(default=timezone.now)
    date_finished = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.coffee_title} ({self.author})"

class Comentario(models.Model):
    endereco = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_publicacao = models.DateTimeField(default=timezone.now)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='comentarios') 

    def _str_(self):
        return f"Comentário de {self.endereco} em {self.cafe}: {self.texto}"
