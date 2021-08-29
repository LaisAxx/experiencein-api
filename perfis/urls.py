from django.urls import path, re_path, include
from perfis import views
from rest_framework.authtoken import views as auth_views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('perfis', views.PerfilViewSet)

urlpatterns = [
	path('', include(router.urls)),
	path('perfil/', views.get_meu_perfil, name='perfil'),
	path('convites/', views.get_convites, name="convites"),
	path('convites/convidar/<int:perfil_id>', views.convidar, name='convidar'),
	path('convites/aceitar/<int:convite_id>', views.aceitar, name='aceitar'),
	path('login/', auth_views.obtain_auth_token, name='login')
]


# from django.urls import path, re_path, include
# from perfis import views
# from rest_framework import views as auth_views
# from rest_framework.routers import DefaultRouter



# router = DefaultRouter()
# router.register('perfis', views.PerfilViewSet)

# urlpatterns = [
# 	path('', include(router.urls)),
# 	path('perfil/', views.get_meu_perfil, name='perfil'),
# 	path('convites/', views.views.get_convites, name='convites'),
# 	path('convite/convidar/<int:perfil_id>', views.convidar, name='convidar'),
# 	path('convite/aceitar/<int:convite_id>', views.aceitar, name='aceitar'),
# 	path('login/', auth_views.obtain_auth_token, name='login')
# ]