from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.lista_recetas, name='lista_recetas'),
    path('inicio/', views.inicio, name='inicio'),
    path('crear/', views.crear_receta, name='crear_receta'),
    path('editar/<int:id>/', views.editar_receta, name='editar_receta'),
    path('borrar/<int:id>/', views.borrar_receta, name='borrar_receta'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='recetas/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Provide a route for /accounts/profile/ to avoid missing-page errors
    path('accounts/profile/', views.inicio, name='profile'),
]