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
     path('cadastro_franquia/', views.CriarFranquiaView.as_view(), name='cadastro_franquia')
]