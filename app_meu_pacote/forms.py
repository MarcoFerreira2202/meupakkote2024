from datetime import datetime
from random import randint
from django import forms
from .models import Encomenda, Funcionario, Morador, Apartamento, Condominio
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['user', 'nomeF', 'condominio','funcaoFuncionario', 'email', 'telefone']
        labels = {'user': 'Usuário', 'nomeF': 'Nome', 'condominio': 'Condomínio', 'funcaoFuncionario': 'Função', 'email': 'E-mail', 'telefone': 'Telefone'}
        widgets = {'user': forms.Select(attrs={'class': 'form-control'}),
                    'nomeF': forms.TextInput(attrs={'class': 'form-control'}),
                    'condominio': forms.Select(attrs={'class': 'form-select'}),
                    'funcaoFuncionario': forms.TextInput(attrs={'class': 'form-control'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'telefone': forms.TextInput(attrs={'class': 'form-control'})}
    def __init__(self, *args, **kwargs):
        super(FuncionarioForm, self).__init__(*args, **kwargs)
        existing_users = Funcionario.objects.all().values_list('user', flat=True)
        self.fields['user'].queryset = User.objects.exclude(id__in=existing_users).order_by('username')

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'endereco', 'telefone', 'email']
        labels = {'nome': 'Nome', 'endereco': 'Endereço', 'telefone': 'Telefone', 'email': 'E-mail'}
        widgets = {'nome': forms.TextInput(attrs={'class': 'form-control'}),
                   'endereco': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'telefone': forms.TextInput(attrs={'class': 'form-control'})}
       
class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['morador', 'descricao', 'data_hora_recebimento']
        labels = {'morador': 'Morador', 'descricao': 'Descrição', 'data_hora_recebimento': 'Data e hora de recebimento'}
        widgets = {'morador': forms.Select(attrs={'class': 'form-select'}),
                   'descricao': forms.TextInput(attrs={'class': 'form-control'}),
                   'data_hora_recebimento': forms.DateTimeInput(),
                   }
    
    def __init__(self, *args, **kwargs):
        # Recebe um argumento "initial" que contém dados para o formulário
        initial = kwargs.get('initial', {})

        super().__init__(*args, **kwargs)

        self.fields['data_hora_recebimento'].initial = datetime.now()
        
    def save(self, user, commit=True):
        encomenda = super(EncomendaForm, self).save(commit=False)
        encomenda.codigo_retirada = str(randint(0,9999)).zfill(4)
        encomenda.funcionario_recebimento = Funcionario.objects.get(user=user)
        if commit:
            encomenda.save()
        return encomenda

        # widgets = {'morador': forms.TextInput(attrs={'class': 'form-control'}),
        #            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
        #            'data_hora_recebimento': forms.TextInput(attrs={'class': 'form-control'})}

class BaixaEncomendaForm(forms.Form):
    codigo_enviado = forms.CharField(label='Código enviado', max_length=4, widget=forms.TextInput(attrs={'class': 'form-control'}))

class UserRegistrationForm(UserCreationForm):
    class Meta:
        models = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100)
    password = forms.CharField(label='Senha', max_length=100, widget=forms.PasswordInput)

class MoradorForm(forms.ModelForm):
    class Meta:
        model = Morador
        fields = ['user', 'nome', 'apartamento', 'email', 'telefone']
        labels = {'user': 'Usuário', 'nome': 'Nome', 'apartamento': 'Apartamento', 'email': 'E-mail', 'telefone': 'Telefone'}
        widgets = {'user': forms.Select(attrs={'class': 'form-control'}),
                    'nome': forms.TextInput(attrs={'class': 'form-control'}),
                    'apartamento': forms.Select(attrs={'class': 'form-control'}),
                    'email': forms.EmailInput(attrs={'class': 'form-control'}),
                    'telefone': forms.TextInput(attrs={'class': 'form-control'})
                    }
    def __init__(self, *args, **kwargs):
        super(MoradorForm, self).__init__(*args, **kwargs)
        #existing_users = Morador.objects.all().values_list('user', flat=True)
        self.fields['user'].queryset = User.objects.exclude(id__in=existing_users).order_by('username')

# formulario morador

class MoradorRegistrationForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    apartamento = forms.ModelChoiceField(queryset=Apartamento.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'nome', 'telefone', 'apartamento')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user    
#def register_morador(request):
#    if request.method == 'POST':
#        form = MoradorForm(request.POST)
#        if form.is_valid():
#            apartamento = form.cleaned_data['apartamento']
#            morador = form.save(commit=False)
#            morador.apartamento = apartamento
#            morador.save()
#            return redirect('algum_url_de_sucesso')
#        else:
            # Tratar o caso de form inválido
#            return render(request, 'register.html', {'form': form})
def register_morador(request):
    if request.method == 'POST':
        form = MoradorForm(request.POST)
        if form.is_valid():
            morador = form.save(commit=False)  # Salva o Morador sem cometer no banco de dados
            apartamento_id = form.cleaned_data.get('apartamento')  # Obtém o id do apartamento do form
            if apartamento_id:
                morador.apartamento = Apartamento.objects.get(id=apartamento_id)  # Atribui o objeto Apartamento ao morador
                morador.save()  # Salva o Morador com o apartamento
                return redirect('algum_url_de_sucesso')
            else:
                form.add_error('apartamento', 'Por favor, selecione um apartamento válido.')  # Adiciona erro se não houver apartamento selecionado
        # Renderiza o formulário novamente com erros
        return render(request, 'register_morador.html', {'form': form})
    else:
        form = MoradorForm()
        return render(request, 'register_morador.html', {'form': form})
