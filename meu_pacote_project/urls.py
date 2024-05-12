"""meu_pacote_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from app_meu_pacote import views as app_meu_pacote_views
from accounts import views as accounts_views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'condominios', app_meu_pacote_views.CondominioViewSet)
router.register(r'funcionarios', app_meu_pacote_views.FuncionarioViewSet)
router.register(r'encomendas', app_meu_pacote_views.EncomendaViewSet)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('buscar_encomendas/', app_meu_pacote_views.BuscarEncomendas.as_view(), name='buscar_encomendas'),
    path('api/', include(router.urls)),
    path('register/', app_meu_pacote_views.register_morador, name='register_morador'),
    path('registro_sucesso/', app_meu_pacote_views.registro_sucesso, name='registro_sucesso'),
    path('admin/', admin.site.urls),
    path('', app_meu_pacote_views.index, name='index'),
    path('encomendas_pendentes/', app_meu_pacote_views.encomendas_pendentes, name='encomendas_pendentes'),
    path('minhas_encomendas/', app_meu_pacote_views.minhas_encomendas, name='minhas_encomendas'),
    path('encomendas_entregues/', app_meu_pacote_views.encomendas_entregues, name='encomendas_entregues'),
    path('cadastrar_encomenda/', app_meu_pacote_views.cadastrar_encomenda, name='cadastrar_encomenda'),
    path('encomenda/<int:encomenda_id>/', app_meu_pacote_views.encomenda, name='encomenda_url'),
    path('logout/', app_meu_pacote_views.logout_view, name='logout'),
    path('cadastrar_morador/', app_meu_pacote_views.cadastrar_morador, name='cadastrar_morador'),
    path('cadastrar_funcionario/', app_meu_pacote_views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('login/', accounts_views.login_view, name='login_view'),
    path('signup/', accounts_views.signup_view, name='signup_view'),
    path('telainicial/', app_meu_pacote_views.encomenda, name='telainicial_url'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
