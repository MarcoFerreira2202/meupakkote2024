from rest_framework import serializers
from .models import Condominio, Funcionario, Apartamento, Morador, Encomenda

class CondominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominio
        fields = '__all__'

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class ApartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartamento
        fields = '__all__'

class MoradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Morador
        fields = '__all__'

class EncomendaSerializer(serializers.ModelSerializer):
  #  foi_entregue = serializers.BooleanField(read_only=True, source='foi_entregue')
    foi_entregue = serializers.BooleanField()

    class Meta:
        model = Encomenda
        fields = '__all__'
