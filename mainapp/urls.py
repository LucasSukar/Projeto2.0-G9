from django.urls import path
from . import views




urlpatterns = [
    path('',views.HomeView.as_view(),name='home' ),
    path('cadastro/',views.CadastroView.as_view(),name='cadastro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('biblioteca/', views.Biblioteca.as_view(), name='biblioteca'),
    path('biblioteca/livro/<int:pk>/', views.LivroEmDetalhe.as_view(), name='livro_detail'),
    path('criarlivro/', views.LivroCreateView.as_view(), name='livro_create'),
    path('atualizar/<int:pk>/', views.LivroUpdateView.as_view(), name='livro_update'),
    path('livro/deletar/<int:pk>/', views.LivroDeleteView.as_view(), name='livro_delete'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('perfil/mudar_senha/', views.MudarSenhaView.as_view(),name='mudar_senha'),
    path('lista_desejos/add/', views.AddListaDesejosView.as_view(), name='add_lista_desejos'),
    path('lista_desejos/', views.ListaDesejosView.as_view(), name='lista_desejos'),
    path('lista_desejos/deletar/<int:livro_id>/', views.RemoverDaListaView.as_view(), name='remove_lista_desejos'),
    path('lista_desejos/add_para_colecao/<int:livro_id>/', views.AddParaColecaoView.as_view(), name='add_book_colecao'),
    path('book_history/', views.BookHistoryView.as_view(), name='book_history'),
    path('remove_history/<int:livro_id>/', views.RemoveFromHistoryView.as_view(), name='remove_history'),
]