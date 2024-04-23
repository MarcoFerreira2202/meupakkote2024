# verificar a integridade dos dados e a relação com o modelo User
from django.test import TestCase
from django.contrib.auth.models import User
from app_meu_pacote.models import Morador, Apartamento, Condominio

class MoradorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Configuração inicial para todos os métodos de teste
        user = User.objects.create_user(username='morador', password='testpass')
        apartamento = Apartamento.objects.create(numero='101')
        Morador.objects.create(user=user, nome="João Silva", apartamento=apartamento, email="joao@exemplo.com", telefone="123456789")

    def test_morador_creation(self):
        morador = Morador.objects.get(id=1)
        self.assertEqual(morador.nome, "João Silva")
        self.assertEqual(morador.user.username, 'morador')

    def test_email_field(self):
        morador = Morador.objects.get(id=1)
        self.assertEqual(morador.email, "joao@exemplo.com")

    def test_telefone_field(self):
        morador = Morador.objects.get(id=1)
        self.assertEqual(morador.telefone, "123456789")
    def setUpTestData(cls):
        # Criação de um condomínio para satisfazer a restrição de chave estrangeira
        condominio = Condominio.objects.create(nome="Condominio Teste", endereco="Endereço Teste", telefone="123456789", email="teste@teste.com")
        
        # Agora criamos o apartamento com o condomínio associado
        apartamento = Apartamento.objects.create(numero='101', condominio=condominio)

        # Continuação da criação dos dados de teste
        #Morador.objects.create(nome="Teste Morador", email="morador@teste.com", telefone="987654321", apartamento=apartamento)
        cls.morador = Morador.objects.create(user=None, nome="Morador Teste", apartamento=apartamento, email="teste@teste.com", telefone="987654321")

    
# app_meu_pacote/tests/test_models.py


class MoradorModelTest(TestCase):
    @classmethod
    
    def setUpTestData(cls):
        # Cria um usuário.
        user = User.objects.create_user(username='testuser', password='12345', email='user@test.com')
        # Certifique-se de criar e associar todas as dependências necessárias
        condominio = Condominio.objects.create(nome="Condominio Exemplo", endereco="Rua Exemplo", telefone="123456789", email="exemplo@exemplo.com")
        apartamento = Apartamento.objects.create(numero="100", condominio=condominio)
        
        cls.morador = Morador.objects.create(user=None, nome="Morador Teste", apartamento=apartamento, email="teste@teste.com", telefone="987654321")

    
    
    def test_morador_creation(self):
        # Teste para verificar se o morador foi criado corretamente
        morador = Morador.objects.get(id=self.morador.id)
        self.assertEqual(morador.nome, "Teste Morador")
        # Adicione outros objetos e configurações necessárias para seus testes
    
    
    

