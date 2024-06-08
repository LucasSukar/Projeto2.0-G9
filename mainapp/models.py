from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Categoria(models.Model):
    tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipo

class Cafe(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    cntt = models.CharField(max_length=15)
    tipo = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cafes')
    isbn = models.CharField(max_length=13, null=True)
    in_collection = models.BooleanField(default=True)
    caracteristicas = models.TextField(blank=True)

    def get_caracteristicas_list(self):
        return self.caracteristicas.split(",")

    def set_caracteristicas_list(self, caracteristicas_list):
        self.caracteristicas = ",".join(caracteristicas_list)

    caracteristicas_list = property(get_caracteristicas_list, set_caracteristicas_list)

    def calcular_media_avaliacoes(self):
        avaliacoes = Avaliacao.objects.filter(cafe=self)
        if avaliacoes.exists():
            media = avaliacoes.aggregate(models.Avg('nota'))['nota__avg']
            return round(media, 2)  # Retorna a média arredondada para 2 casas decimais
        return None

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(choices=[(i, f'{i} Estrelas') for i in range(6)])
    data_avaliacao = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'cafe')

    def __str__(self):
        return f"Avaliação de {self.user} para {self.cafe}: {self.nota} Estrelas"

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
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='novidades')

    def __str__(self):
        return f"Novidade de {self.endereco} em {self.cafe}: {self.texto}"

class Favorito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

class ListaDesejo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

class Frequentado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
