from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cafe, Categoria
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Cafe, Categoria, ListaDesejos
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from .models import Cafe,BookHistory
from django.utils import timezone

class HomeView(View):
    def get(self, request):
        contexto = {'user': request.user if request.user.is_authenticated else None}
        if request.user.is_authenticated:
            cafes_usuario = Cafe.objects.filter(usuario=request.user)
            total_cafes = cafes_usuario.count()
            generos_ordenados = cafes_usuario.values('genero__genero').annotate(total=Count('genero')).order_by('-total')

            if generos_ordenados:
                generos_mais_comuns = generos_ordenados.filter(total=generos_ordenados.first()['total'])
                generos_menos_comuns = generos_ordenados.filter(total=generos_ordenados.last()['total'])

                contexto['genero_mais_comum'] = ', '.join([g['genero__genero'] for g in generos_mais_comuns])
                contexto['genero_menos_comum'] = ', '.join([g['genero__genero'] for g in generos_menos_comuns])
            else:
                contexto['genero_mais_comum'] = 'Indisponível'
                contexto['genero_menos_comum'] = 'Indisponível'

            contexto['total_cafes'] = total_cafes

        return render(request, 'mainapp/home.html', contexto)

    
class CadastroView(View):
    def get(self, request):
        return render(request, 'mainapp/cadastro.html')
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')  
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'mainapp/cadastro.html', {
                'error': 'Usuário e senha são campos obrigatórios.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'mainapp/cadastro.html', {
                'error': 'Nome de usuário já existe.'
            })

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return redirect('login')  

class LoginView(LoginView):
    template_name = 'mainapp/login.html'  
    redirect_authenticated_user = True  
    next_page = reverse_lazy('home')
   
    
class LogoutView(View):

    @method_decorator(csrf_protect)
    def post(self, request):
        logout(request)
        return redirect('home')

class Biblioteca(View):
    def get(self, request):
        if not request.user.is_authenticated:
            
            return redirect('home')
        else:
            cafes = Cafe.objects.filter(usuario=request.user, in_collection=True)
            #for cafe in cafes:
                #book_info = fetch_book_info_by_title(cafe.titulo)
                #if book_info:
                    #cafe.cover_url = book_info.get('cover_url')
            return render(request, 'mainapp/biblioteca.html', {'cafes': cafes})


class CafesEmDetalhe(LoginRequiredMixin,View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        book_info = None
       
        if not cafe.isbn:
            #book_info = fetch_book_info_by_title(cafe.titulo)
            if book_info:
                cafe.isbn = book_info.get('isbn')
                cafe.cover_url = book_info.get('cover_url')
                cafe.save()
            else:
            
                cafe.cover_url = book_info.get('cover_url') if cafe.isbn else None
        return render(request, 'mainapp/cafe_detail.html', {'cafe': cafe})


class CafeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'mainapp/cafe_form.html', {'categorias': categorias})

    def post(self, request):
        titulo = request.POST.get('titulo').strip()
        autor = request.POST.get('autor').strip()
        anopublicado = request.POST.get('anopublicado').strip()
        genero_id = request.POST.get('genero').strip()
        
        if not titulo or not autor or not anopublicado:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cafe_create')

        if Cafe.objects.filter(titulo__iexact=titulo, usuario=request.user).exists():
            messages.error(request, 'Uma cafeteria com este nome já existe na sua biblioteca.')
            return redirect('cafe_create')

        genero = get_object_or_404(Categoria, id=genero_id)
        Cafe.objects.create(titulo=titulo, autor=autor, anopublicado=anopublicado, genero=genero, usuario=request.user)
        messages.success(request, 'cafeteria adicionada com sucesso!')
        return redirect('biblioteca')


class CafeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        status_leitura = cafe.status_leitura
        return render(request, 'mainapp/cafe_update.html', {'cafe': cafe, 'categorias': Categoria.objects.all(), 'status_leitura': status_leitura})

    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.titulo = request.POST.get('titulo')
        cafe.autor = request.POST.get('autor')
        cafe.anopublicado = request.POST.get('anopublicado')
        cafe.genero = get_object_or_404(Categoria, pk=request.POST.get('genero'))
        novo_status_leitura = request.POST.get('status_leitura')

        if cafe.status_leitura != 'NL' and novo_status_leitura == 'NL':
            if BookHistory.objects.filter(user=request.user, book_title=cafe.titulo, author=cafe.autor).exists():
                BookHistory.objects.filter(user=request.user, book_title=cafe.titulo, author=cafe.autor).delete()
                messages.success(request, 'cafeteria editada com sucesso!')

        elif novo_status_leitura in ['L', 'EL']:
            if not BookHistory.objects.filter(user=request.user, book_title=cafe.titulo, author=cafe.autor).exists():
                BookHistory.objects.create(
                    user=request.user,
                    book_title=cafe.titulo,
                    author=cafe.autor,
                )
                messages.success(request, 'cafeteria editada com sucesso!')

        cafe.status_leitura = novo_status_leitura
        cafe.save()
        return redirect('biblioteca')

class CafeDeleteView(LoginRequiredMixin,View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        return render(request, 'mainapp/cafe_confirm_delete.html', {'cafe': cafe})

    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.delete()
        return redirect('biblioteca')

class PerfilView(LoginRequiredMixin,View):
    def get(self, request):
        if not request.user.is_authenticated:
            
            return redirect('home')
        else:
            usuario=request.user.username
            email=request.user.email
            context = {'usuario': usuario, 'email': email}
            return render(request, 'mainapp/perfil.html', context)

class MudarSenhaView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'mainapp/mudar_senha.html')

    def post(self, request):
        senha_antiga = request.POST.get('senha_antiga')
        nova_senha = request.POST.get('nova_senha')
        confirmar = request.POST.get('confirmar')

        if not request.user.check_password(senha_antiga):
            messages.error(request, 'Sua senha antiga foi digitada errado. Tente novamente.')
        elif nova_senha != confirmar:
            messages.error(request, 'Por favor, digite sua senha nova igual ao escrito no primeiro campo.')
        else:
            request.user.password = make_password(nova_senha)
            request.user.save()
            update_session_auth_hash(request, request.user)  
            messages.success(request, 'Sua senha foi atualizada com sucesso!')
            return redirect('home')

        return render(request, 'mainapp/mudar_senha.html')
    
class AddListaDesejosView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'mainapp/add_lista.html', {'categorias': categorias})

    def post(self, request):
        titulo = request.POST.get('titulo').strip()
        autor = request.POST.get('autor').strip()
        anopublicado = request.POST.get('anopublicado').strip()
        genero_id = request.POST.get('genero').strip()
        
        if not titulo or not autor or not anopublicado:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cafe_create')

        genero = get_object_or_404(Categoria, id=genero_id)
        
        
        cafe = Cafe(titulo=titulo, autor=autor, anopublicado=anopublicado, genero=genero, in_wishlist=True, in_collection=False,usuario=request.user)
        cafe.save()
        
       
        wishlist, created = ListaDesejos.objects.get_or_create(usuario=request.user)
        wishlist.cafes.add(cafe)  
        
        messages.success(request, "cafeteria adicionada à lista de desejos com sucesso.")
        return redirect('lista_desejos')
        
        

class ListaDesejosView(LoginRequiredMixin, View):
    def get(self, request):
        wishlist, created = ListaDesejos.objects.get_or_create(usuario=request.user)
        cafes_desejados = wishlist.cafes.all()
        return render(request, 'mainapp/lista_desejos.html', {'cafes_desejados': cafes_desejados})    

class RemoverDaListaView(LoginRequiredMixin, View):
    def post(self, request,**kwargs):
        cafe_id = kwargs.get('cafe_id')
        cafe = get_object_or_404(Cafe, id=cafe_id)
        wishlist = ListaDesejos.objects.get(usuario=request.user)
        wishlist.cafes.remove(cafe)
        cafe.delete()
        messages.success(request, "cafeteria removida da lista de desejos com sucesso.")
        return redirect('lista_desejos')
    
class AddParaColecaoView(LoginRequiredMixin, View):
    def post(self, request, cafe_id):
        cafe = get_object_or_404(Cafe, id=cafe_id, usuario=request.user)
        cafe.in_wishlist = False
        cafe.in_collection = True
        cafe.save()
        
        wishlist = ListaDesejos.objects.filter(usuario=request.user).first()
        if wishlist:
            wishlist.cafes.remove(cafe)

        messages.success(request, "cafeteria adicionada com sucesso.")
        return redirect('lista_desejos')  
    

class BookHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        book_history = BookHistory.objects.filter(user=request.user)
        return render(request, 'mainapp/book_history.html', {'book_history': book_history})

    def post(self, request, cafe_id):
        cafe = get_object_or_404(Cafe, id=cafe_id, usuario=request.user)
        BookHistory.objects.create(
            user=request.user,
            book_title=cafe.titulo,
            author=cafe.autor,
            date_started=cafe.date_added,
            date_finished=timezone.now()
        )
        cafe.delete()      
        return redirect('book_history')
    
class RemoveFromHistoryView(View):
    def post(self, request, cafe_id):
        book = get_object_or_404(BookHistory, pk=cafe_id, user=request.user)
        book.delete()
        messages.success(request, "cafeteria removida do histórico.")
        return redirect('book_history')
