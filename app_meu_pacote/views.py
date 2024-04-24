from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import Encomenda, Morador, Funcionario, Condominio
from .forms import EncomendaForm, UserRegistrationForm, MoradorForm, FuncionarioForm, BaixaEncomendaForm
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Encomenda, Funcionario, Apartamento
from .forms import BaixaEncomendaForm
# meu_app/views.py
from rest_framework import viewsets
from .models import Condominio, Funcionario, Encomenda
from .serializers import CondominioSerializer, FuncionarioSerializer, EncomendaSerializer
# view para buscar encomendas
from rest_framework.views import APIView
from rest_framework.response import Response
#from django.shortcuts import get_object_or_404
# autenticação e autorização - proteção na classe Buscar encomendas
from rest_framework.permissions import IsAuthenticated
# view generica
from django.views.generic import TemplateView
# adicionando morador
from .forms import MoradorRegistrationForm, MoradorForm
from django import forms




class CondominioViewSet(viewsets.ModelViewSet):
    queryset = Condominio.objects.all()
    serializer_class = CondominioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer

class EncomendaViewSet(viewsets.ModelViewSet):
    queryset = Encomenda.objects.all()
    serializer_class = EncomendaSerializer

class BuscarEncomendas(APIView):
    # templatename
    template_name = 'buscar_encomendas.html'
    permission_classes = [IsAuthenticated]
    # O resto da sua view como definido anteriomente
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione sua lógica para buscar encomendas aqui
        return context
    def get(self, request, *args, **kwargs):
        morador = get_object_or_404(Morador, user=request.user)
        encomendas = Encomenda.objects.filter(morador=morador)
        serializer = EncomendaSerializer(encomendas, many=True)
        return Response(serializer.data)

#classe morador
class MoradorForm(forms.ModelForm):
    class Meta:
        model = Morador
        fields = ['user', 'nome', 'apartamento', 'email', 'telefone']

    def save(self, commit=True):
        morador = super().save(commit=False)
        # certifique-se de que apartamento é fornecido ou trate de forma adequada
        if self.cleaned_data['apartamento'] is None:
            raise forms.ValidationError("Apartamento é necessário")
        if commit:
            morador.save()
        return morador

#ajuste APi
def buscar_encomendas_page(request):
    # Esta view é para renderizar a página HTML
    return render(request, 'buscar_encomendas.html')


#registro de morador
def register_morador(request):
    if request.method == 'POST':
        form = MoradorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        #    return redirect('url_para_página_de_sucesso')
        #else:
            # Aqui é importante para ver os erros de validação
        #    print(form.errors)
#    else:
#        form = MoradorForm()
#    return render(request, 'register_morador.html', {'form': form})
#           return redirect('login')
    else:
        form = MoradorRegistrationForm()
    return render(request, 'register_morador.html', {'form': form})

#renderizar views

def my_view(request):
    # Seu código aqui
    return render(request, 'my_template.html', context)



















# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login_view')
    return render(request, 'index.html')

def cadastrar_encomenda(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    if request.method == 'POST':
        form = EncomendaForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            msg_sucesso = f'Encomenda "{form.instance.descricao}" para "{form.instance.morador}" cadastrada com sucesso!'
            form = EncomendaForm()
            return render(request, 'cadastrar_encomenda.html', {'msg': msg_sucesso, 'form': form})
    else:
        form = EncomendaForm()
    return render(request, 'cadastrar_encomenda.html', {'form': form})

def encomendas_pendentes(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    encomendas = Encomenda.objects.filter(data_hora_entrega=None)
    context = {'encomendas': encomendas}
    return render(request, 'encomendas_pendentes.html', context)

def encomenda(request, encomenda_id):
    encomenda = get_object_or_404(Encomenda, id=encomenda_id)

    if request.method == 'POST':
        form = BaixaEncomendaForm(request.POST)
        if form.is_valid():
            codigo_enviado = str(form.cleaned_data['codigo_enviado'])
            if codigo_enviado == encomenda.codigo_retirada:
                try:
                    funcionario = Funcionario.objects.get(user=request.user)
                except ObjectDoesNotExist:
                    # Tratar o caso de o Funcionario não existir
                    return render(request, 'error.html', {'message': 'Funcionário não encontrado.'})

                encomenda.data_hora_entrega = timezone.now()
                encomenda.funcionario_entrega = funcionario
                encomenda.save()
                return render(request, 'confirmacao.html', {'encomenda': encomenda})
            else:
                return render(request, 'encomenda.html', {'form': form, 'encomenda': encomenda, 'error': 'Código de retirada inválido.'})
    else:
        form = BaixaEncomendaForm()
        return render(request, 'encomenda.html', {'form': form, 'encomenda': encomenda})























def encomendas_entregues(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    encomendas = Encomenda.objects.filter(data_hora_entrega != None)
    context = {'encomendas': encomendas}
    return render(request, 'encomendas_entregues.html', context)

def minhas_encomendas(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    # encomendas = Encomenda.objects.filter(morador=request.user)  precisa arrumar!!!!!!!
    encomendas = Encomenda.objects.all().order_by('data_hora_recebimento').reverse()
    moradores = Morador.objects.all()
    context = {'encomendas': encomendas, 'moradores': moradores}
    return render(request, 'minhas_encomendas.html', context)

def cadastrar_funcionario(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            msg_sucesso = f'Funcionário "{form.instance.nomeF}" cadastrado com sucesso!'
            form = FuncionarioForm()
            return render(request, 'cadastrar_funcionario.html', {'msg': msg_sucesso, 'form': form})
    else:
        form = FuncionarioForm()
    return render(request, 'cadastrar_funcionario.html', {'form': form})


def cadastrar_condominio(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    if request.method == 'POST':
        form = CondominioForm(request.POST)
        if form.is_valid():
            form.save()
            msg_sucesso = f'Condominio "{form.instance.nome}" cadastrado com sucesso!'
            form = CondominioForm()
            return render(request, 'cadastrar_condominio.html', {'msg': msg_sucesso, 'form': form})
    else:
        form = CondominioForm()
    return render(request, 'cadastrar_condominio.html', {'form': form})

def cadastrar_morador(request):
    if not request.user.is_authenticated:
        return redirect('index') # issue ---> precisa redirecionar para a página de login
    if request.method == 'POST':
        form = MoradorForm(request.POST)
        if form.is_valid():
            form.save()
            msg_sucesso = f'Morador "{form.instance.nome}" cadastrado com sucesso!'
            form = MoradorForm()
            return render(request, 'cadastrar_morador.html', {'msg': msg_sucesso, 'form': form})
    else:
        form = MoradorForm()
    return render(request, 'cadastrar_morador.html', {'form': form})
# cadastro de morador


def lista_funcionarios(request):
    funcionarios = Funcionario.objects.all()
    context = {'funcionarios': funcionarios}
    return render(request, 'lista_funcionarios.html', context)


#def login(request):
 #   if request.method == 'POST':
  #      form = UserCreationForm(request.POST)
   #     if form.is_valid():
    #        user = form.save()
     #       login(request, user)
      #      return redirect('index')
    #else:
     #   form = UserCreationForm()
      #  return render(request, 'login.html', {'form': form})



"""
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
    #     if request.POST['username'] == 'admin' and request.POST['password'] == 'admin':
    #         return render(request, 'index.html')
    #     else:
    #         return render(request, 'login.html', {'msg': 'Usuário ou senha inválidos'})
    # return render(request, 'login.html')
"""



class LoginView(UserRegistrationForm):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Invalid credentials'})

def logout_view(request):
    logout(request)
    return redirect('index')

def error404(request, exception):
    return redirect('index')
    
