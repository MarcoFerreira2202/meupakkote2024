from django.contrib import admin
from .models import Condominio, Apartamento, Morador, Encomenda, Funcionario
# acesso via interface administrativa
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CondominioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'email')
    search_fields = ('nome', 'endereco', 'telefone', 'email')
admin.site.register(Condominio, CondominioAdmin)

class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'condominio')
    search_fields = ('numero', 'condominio_nome')
admin.site.register(Apartamento, ApartamentoAdmin)

class MoradorAdmin(admin.ModelAdmin):
    #list_display = ('nome', 'apartamento', 'email', 'telefone')
    #search_fields = ('nome', 'apartamento_numero', 'email', 'telefone')
    list_display = ('nome', 'email', 'telefone', 'user')
    search_fields = ('nome', 'email', 'telefone')
    raw_id_fields = ('user',)  # Facilita a vinculação do usuário
admin.site.register(Morador, MoradorAdmin)

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','nomeF', 'condominio', 'funcaoFuncionario', 'email', 'telefone')
    search_fields = ('user__username', 'nomeF', 'condominio__nome', 'funcaoFuncionario', 'email', 'telefone')
admin.site.register(Funcionario, FuncionarioAdmin)

class EncomendaAdmin(admin.ModelAdmin):
    list_display = ('morador', 'descricao', 'data_hora_recebimento', 'data_hora_entrega')
    search_fields = ('morador', 'descricao', 'data_hora_recebimento', 'data_hora_entrega')
admin.site.register(Encomenda, EncomendaAdmin)
#possivel duplicidade em models.py
#class Morador(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    nome = models.CharField(max_length=100)
#    # Substitua 'Apartamento' pelo seu modelo de apartamento
#    apartamento = models.ForeignKey('Apartamento', on_delete=models.CASCADE, related_name='moradores')
#    email = models.EmailField()
#    telefone = models.CharField(max_length=20)

    # Outros campos e métodos conforme necessário