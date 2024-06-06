from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('biblioteca/', views.Biblioteca.as_view(), name='biblioteca'),
    path('biblioteca/cafe/<int:pk>/', views.CafesEmDetalhe.as_view(), name='cafe_detail'),
    path('criarcafe/', views.CafeCreateView.as_view(), name='cafe_create'),
    path('atualizar/<int:pk>/', views.CafeUpdateView.as_view(), name='cafe_update'),
    path('cafe/deletar/<int:pk>/', views.CafeDeleteView.as_view(), name='cafe_delete'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/mudar_senha/', views.MudarSenhaView.as_view(), name='mudar_senha'),
    path('adicionar_comentario/<int:cafe_id>/', views.AdicionarComentarioView.as_view(), name='adicionar_comentario'),
    path('deletar_comentario/<int:comentario_id>/', views.DeletarComentarioView.as_view(), name='deletar_comentario'),
    path('all/', views.AllCoffes.as_view(), name='all'),
    path('avaliacao/<int:cafe_id>/', views.AvaliacaoCafeteriaView.as_view(), name='avaliacao'),
    path('adicionar_frequente/<int:pk>/', views.AdicionarFrequenteView.as_view(), name='adicionar_frequente'),
    path('cafes_por_categoria/<int:categoria_id>/', views.CafesPorCategoriaView.as_view(), name='cafes_por_categoria'),
    path('sobre/', views.SobreView.as_view(), name='sobre'),
    path('favoritos/<int:pk>/', views.MarcarCafeteriaFavoritaView.as_view(), name='favoritos'),
    path('lista_desejo/<int:pk>/', views.ListaDesejoView.as_view(), name='lista_desejo'), 
    path('adicionar_novidade/<int:cafe_id>/', views.AdicionarNovidadeView.as_view(), name='adicionar_novidade'),
    path('deletar_novidade/<int:novidade_id>/', views.DeletarNovidadeView.as_view(), name='deletar_novidade'),
]