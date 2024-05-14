from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy,  reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Count
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Cafe, Categoria, ListaDesejos, Franquia, CoffeeHistory, Comentario
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.http import HttpResponseRedirect
    
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
            return render(request, 'mainapp/biblioteca.html', {'cafes': cafes})


class CafesEmDetalhe(LoginRequiredMixin,View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        coffee_info = None
       
        if not cafe.isbn:
            if coffee_info:
                cafe.isbn = coffee_info.get('isbn')
                cafe.cover_url = coffee_info.get('cover_url')
                cafe.save()
            else:
            
                cafe.cover_url = coffee_info.get('cover_url') if cafe.isbn else None
        return render(request, 'mainapp/cafe_detail.html', {'cafe': cafe})


class CafeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'mainapp/cafe_form.html', {'categorias': categorias})

    def post(self, request):
        nome = request.POST.get('nome').strip()
        autor = request.POST.get('autor').strip()
        anopublicado = request.POST.get('anopublicado').strip()
        genero_id = request.POST.get('genero').strip()
        vezes_visitado = request.POST.get('vezes_visitado')

        if not nome or not autor or not anopublicado or not vezes_visitado:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cafe_create')

        if Cafe.objects.filter(nome__iexact=nome, usuario=request.user).exists():
            messages.error(request, 'Uma cafeteria com este nome já existe na sua biblioteca.')
            return redirect('cafe_create')

        genero = get_object_or_404(Categoria, id=genero_id)
        Cafe.objects.create(nome=nome, autor=autor, anopublicado=anopublicado, vezes_visitado=vezes_visitado, genero=genero, usuario=request.user)
        messages.success(request, 'Cafeteria adicionada com sucesso!')
        return redirect('biblioteca')

class CafeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        status_cafeteria = cafe.status_cafeteria
        return render(request, 'mainapp/cafe_update.html', {'cafe': cafe, 'categorias': Categoria.objects.all(), 'status_cafeteria': status_cafeteria})

    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.nome = request.POST.get('nome')
        cafe.autor = request.POST.get('autor')
        cafe.anopublicado = request.POST.get('anopublicado')
        cafe.vezes_visitado = request.POST.get('vezes_visitado')
        cafe.genero = get_object_or_404(Categoria, pk=request.POST.get('genero'))
        novo_status_cafeteria = request.POST.get('status_cafeteria')

        if cafe.status_cafeteria != 'NL' and novo_status_cafeteria == 'NL':
            if CoffeeHistory.objects.filter(user=request.user, coffee_title=cafe.nome, author=cafe.autor).exists():
                CoffeeHistory.objects.filter(user=request.user, coffee_title=cafe.nome, author=cafe.autor).delete()
                messages.success(request, 'cafeteria editada com sucesso!')

        elif novo_status_cafeteria in ['EL']:
            if not CoffeeHistory.objects.filter(user=request.user, coffee_title=cafe.nome, author=cafe.autor).exists():
                CoffeeHistory.objects.create(
                    user=request.user,
                    coffee_title=cafe.nome,
                    author=cafe.autor,
                )
                messages.success(request, 'cafeteria editada com sucesso!')

        cafe.status_cafeteria = novo_status_cafeteria
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
        nome = request.POST.get('nome').strip()
        autor = request.POST.get('autor').strip()
        anopublicado = request.POST.get('anopublicado').strip()
        genero_id = request.POST.get('genero').strip()
        
        if not nome or not autor or not anopublicado:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cafe_create')

        genero = get_object_or_404(Categoria, id=genero_id)
        
        
        cafe = Cafe(nome=nome, autor=autor, anopublicado=anopublicado, genero=genero, in_wishlist=True, in_collection=False,usuario=request.user)
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
    

class CoffeeHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        coffee_history = CoffeeHistory.objects.filter(user=request.user)
        return render(request, 'mainapp/coffee_history.html', {'coffee_history': coffee_history})

    def post(self, request, cafe_id):
        cafe = get_object_or_404(Cafe, id=cafe_id, usuario=request.user)
        CoffeeHistory.objects.create(
            user=request.user,
            coffee_title=cafe.nome,
            author=cafe.autor,
            date_started=cafe.date_added,
            date_finished=timezone.now()
        )
        cafe.delete()      
        return redirect('coffee_history')
    
class RemoveFromHistoryView(View):
    def post(self, request, cafe_id):
        coffee = get_object_or_404(CoffeeHistory, pk=cafe_id, user=request.user)
        coffee.delete()
        messages.success(request, "cafeteria removida do histórico.")
        return redirect('coffee_history')
    
class CriarFranquiaView(View):
    def get(self, request):
        contexto = {'categorias': Categoria.objects.all()}
        return render(request, 'mainapp/cadastro_franquia.html', contexto)

class AdicionarComentarioView(LoginRequiredMixin, View):
    def get(self, request, cafe_id):
        cafe = get_object_or_404(Cafe, id=cafe_id)
        return render(request, 'mainapp/adicionar_comentario.html', {'cafe': cafe})

    def post(self, request, cafe_id):
        texto = request.POST.get('texto').strip()
        cafe = get_object_or_404(Cafe, id=cafe_id)

        if not texto:
            messages.error(request, 'Por favor, adicione um texto ao comentário.')
            return redirect('adicionar_comentario', cafe_id=cafe_id)

        Comentario.objects.create(autor=request.user, texto=texto, cafe=cafe)
        messages.success(request, 'Comentário adicionado com sucesso.')
        return redirect('cafe_detail', pk=cafe_id)

class DeletarComentarioView(LoginRequiredMixin, View):
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id)
        comentario.delete()
        messages.success(request, 'Comentário removido com sucesso.')
        return redirect('cafe_detail', pk=comentario.cafe.id)