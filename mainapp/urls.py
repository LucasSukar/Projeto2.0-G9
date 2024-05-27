from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home' ),
    path('cadastro/',views.CadastroView.as_view(),name='cadastro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('biblioteca/', views.Biblioteca.as_view(), name='biblioteca'),
    path('biblioteca/cafe/<int:pk>/', views.CafesEmDetalhe.as_view(), name='cafe_detail'),
    path('criarcafe/', views.CafeCreateView.as_view(), name='cafe_create'),
    path('atualizar/<int:pk>/', views.CafeUpdateView.as_view(), name='cafe_update'),
    path('cafe/deletar/<int:pk>/', views.CafeDeleteView.as_view(), name='cafe_delete'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/mudar_senha/', views.MudarSenhaView.as_view(),name='mudar_senha'),
    path('lista_desejos/add/', views.AddListaDesejosView.as_view(), name='add_lista_desejos'),
    path('lista_desejos/', views.ListaDesejosView.as_view(), name='lista_desejos'),
    path('lista_desejos/deletar/<int:cafe_id>/', views.RemoverDaListaView.as_view(), name='remove_lista_desejos'),
    path('lista_desejos/add_para_colecao/<int:cafe_id>/', views.AddParaColecaoView.as_view(), name='add_coffee_colecao'),
    path('coffee_history/', views.CoffeeHistoryView.as_view(), name='coffee_history'),
    path('remove_history/<int:cafe_id>/', views.RemoveFromHistoryView.as_view(), name='remove_history'),
    path('adicionar_comentario/<int:cafe_id>/', views.AdicionarComentarioView.as_view(), name='adicionar_comentario'),
    path('deletar_comentario/<int:comentario_id>/', views.DeletarComentarioView.as_view(), name='deletar_comentario'),
    path('all/',views.AllCoffes.as_view(),name='all'),
    path('avaliacao/<int:cafe_id>/', views.AvaliacaoCafeteriaView.as_view(), name='avaliacao'),
    path('frequente/adicionar/<int:cafe_id>/', views.AdicionarFrequenteView.as_view(), name='adicionar_frequente'),
    path('cafes_por_categoria/<int:categoria_id>/', views.CafesPorCategoriaView.as_view(), name='cafes_por_categoria'),
    path('sobre/', views.SobreView.as_view(), name='sobre'),
]