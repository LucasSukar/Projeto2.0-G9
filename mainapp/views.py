from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy,  reverse
from django.contrib.auth import logout
from django.db.models import Count, F
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Cafe, Categoria, Comentario, Novidade
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType    
from django.contrib.auth.models import User, Permission
    
class HomeView(View):
    def get(self, request):
        contexto = {'user': request.user if request.user.is_authenticated else None}

        if request.user.is_authenticated:
            cafes_usuario = Cafe.objects.filter(usuario=request.user)
            total_cafes = cafes_usuario.count()
            tipos_ordenados = cafes_usuario.values('tipo__tipo').annotate(total=Count('tipo')).order_by('-total')

            if tipos_ordenados.exists(): 
                tipo_mais_comum = tipos_ordenados.first()
                tipo_menos_comum = tipos_ordenados.last()

                if tipo_mais_comum['total'] > 0:
                    contexto['tipo_mais_comum'] = tipo_mais_comum['tipo__tipo']
                else:
                    contexto['tipo_mais_comum'] = 'Indisponível'

                if tipo_menos_comum['total'] > 0:
                    contexto['tipo_menos_comum'] = tipo_menos_comum['tipo__tipo']
                else:
                    contexto['tipo_menos_comum'] = 'Indisponível'
            else:
                contexto['tipo_mais_comum'] = 'Indisponível'
                contexto['tipo_menos_comum'] = 'Indisponível'

            contexto['total_cafes'] = total_cafes

        return render(request, 'mainapp/home.html', contexto)
class CadastroView(View):
    def get(self, request):
        return render(request, 'mainapp/cadastro.html')
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')  
        password = request.POST.get('password')
        is_admin = True if request.POST.get('is_admin') == 'cafe' else False

        if is_admin:
            try:
                permission1 = Permission.objects.get(codename='cafe')
            except:
                content_type = ContentType.objects.get_for_model(User)
                permission1 = Permission.objects.create(
                    codename='cafe',
                    name='cafe',
                    content_type=content_type,
                )
        else:
            permission1 = ''

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
        if permission1 != '':
            user.user_permissions.add(permission1)
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
            cafes = Cafe.objects.filter(usuario=request.user, in_collection=True).order_by(F('is_frequente').desc(nulls_last=True))

            return render(request, 'mainapp/biblioteca.html', {'cafes': cafes})


class CafesEmDetalhe(LoginRequiredMixin, View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        if cafe.usuario == request.user:
            is_owner = True
        else:
            is_owner = False
        coffee_info = None
        if not cafe.isbn:
            if coffee_info:
                cafe.isbn = coffee_info.get('isbn')
                cafe.cover_url = coffee_info.get('cover_url')
                cafe.save()
            else:
                cafe.cover_url = coffee_info.get('cover_url') if cafe.isbn else None
        return render(request, 'mainapp/cafe_detail.html', {'cafe': cafe, 'is_owner': is_owner})

class CafeCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categorias = Categoria.objects.all()
        return render(request, 'mainapp/cafe_form.html', {'categorias': categorias})

    def post(self, request):
        nome = request.POST.get('nome').strip()
        endereco = request.POST.get('endereco').strip()
        cntt = request.POST.get('cntt').strip()
        caracteristicas = request.POST.get('caracteristicas').strip()

        if not nome or not endereco or not cntt or not caracteristicas:
            messages.error(request, 'Todos os campos são obrigatórios.')
            return redirect('cafe_create')

        if Cafe.objects.filter(nome__iexact=nome, usuario=request.user).exists():
            messages.error(request, 'Uma cafeteria com este nome já existe na sua biblioteca.')
            return redirect('cafe_create')

        Cafe.objects.create(nome=nome, endereco=endereco, cntt=cntt, usuario=request.user, caracteristicas=caracteristicas)
        messages.success(request, 'Cafeteria adicionada com sucesso!')
        return redirect('biblioteca')

class CafeUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        status_cafeteria = cafe.status_cafeteria
        return render(request, 'mainapp/cafe_update.html', {
            'cafe': cafe,
            'categorias': Categoria.objects.all(),
            'status_cafeteria': status_cafeteria
        })

    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.nome = request.POST.get('nome')
        cafe.endereco = request.POST.get('endereco')
        cafe.cntt = request.POST.get('cntt')
        cafe.tipo_id = request.POST.get('categoria')
        caracteristicas = request.POST.get('caracteristicas').strip()
        cafe.caracteristicas = caracteristicas
        if 'status_cafeteria' in request.POST:
            cafe.status_cafeteria = request.POST.get('status_cafeteria')
        cafe.save()
        messages.success(request, 'Cafeteria atualizada com sucesso!')
        return redirect('home')  

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
        Comentario.objects.create(endereco=request.user, texto=texto, cafe=cafe)
        messages.success(request, 'Comentário adicionado com sucesso.')
        return redirect('cafe_detail', pk=cafe_id)

class DeletarComentarioView(LoginRequiredMixin, View):
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id)
        if comentario.endereco == request.user:
            is_author = True
        else:
            is_author = False
        if is_author:
            comentario.delete()
            messages.success(request, 'Comentário removido com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir este comentário.')
        return redirect('cafe_detail', pk=comentario.cafe.id)

class AllCoffes(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')
        else:
            cafes = Cafe.objects.all()
            caracteristica_selecionada = request.GET.get('caracteristicas')
            todas_caracteristicas = []
            for cafe in cafes:
                for caracteristica in cafe.caracteristicas.split(","):
                    if caracteristica.strip() not in todas_caracteristicas:
                        todas_caracteristicas.append(caracteristica.strip())
            if caracteristica_selecionada:
                cafes = cafes.filter(caracteristicas__icontains=caracteristica_selecionada)
            return render(request, 'mainapp/all.html', {'cafes': cafes, 'todas_caracteristicas': todas_caracteristicas})
        
class AvaliacaoCafeteriaView(LoginRequiredMixin, View):
    def get(self, request, cafe_id):
        cafe = Cafe.objects.get(pk=cafe_id)
        return render(request, 'mainapp/avaliacao.html', {'cafe': cafe})
    def post(self, request, cafe_id):
        cafe = Cafe.objects.get(pk=cafe_id)
        avaliacao = int(request.POST.get('avaliacao'))
        if cafe.avaliacao:
            cafe.avaliacao = avaliacao
        else:
            cafe.avaliacao = avaliacao
        cafe.save()
        return redirect('cafe_detail', pk=cafe_id)
    
class AdicionarFrequenteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.is_frequente = not cafe.is_frequente
        cafe.save()
        return HttpResponseRedirect(reverse('cafe_detail', kwargs={'pk': pk}))
    
class CafesPorCategoriaView(View):
    def get(self, request, categoria_id):
        categoria = get_object_or_404(Categoria, pk=categoria_id)
        cafes = Cafe.objects.filter(tipo=categoria)
        return render(request, 'mainapp/cafes_por_categoria.html', {'categoria': categoria, 'cafes': cafes})

class SobreView(View):
    def get(self, request):
        return render(request, 'mainapp/sobre.html')
    
class MarcarCafeteriaFavoritaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.is_favorita = not cafe.is_favorita
        cafe.save()
        return HttpResponseRedirect(reverse('cafe_detail', kwargs={'pk': pk}))

class ListaDesejoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cafe = get_object_or_404(Cafe, pk=pk)
        cafe.is_wish = not cafe.is_wish
        cafe.save()
        return HttpResponseRedirect(reverse('cafe_detail', kwargs={'pk': pk}))

class AdicionarNovidadeView(LoginRequiredMixin, View):
    def get(self, request, cafe_id):
        cafe = get_object_or_404(Cafe, id=cafe_id)
        return render(request, 'mainapp/adicionar_novidade.html', {'cafe': cafe})
    def post(self, request, cafe_id):
        texto = request.POST.get('texto').strip()
        cafe = get_object_or_404(Cafe, id=cafe_id)
        if not texto:
            messages.error(request, 'Por favor, adicione um texto à novidade.')
            return redirect('adicionar_novidade', cafe_id=cafe_id)
        Novidade.objects.create(endereco=request.user, texto=texto, cafe=cafe)
        messages.success(request, 'Novidade adicionada com sucesso.')
        return redirect('cafe_detail', pk=cafe_id)

class DeletarNovidadeView(LoginRequiredMixin, View):
    def post(self, request, novidade_id):
        novidade = get_object_or_404(Novidade, id=novidade_id)
        if novidade.endereco == request.user:
            is_author = True
        else:
            is_author = False
        if is_author:
            novidade.delete()
            messages.success(request, 'Novidade removida com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir esta novidade.')
        return redirect('cafe_detail', pk=novidade.cafe.id)