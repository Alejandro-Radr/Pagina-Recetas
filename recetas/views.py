from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseForbidden

from .models import Receta
from .forms import RecetaForm


def lista_recetas(request):
    # Mostrar todas las recetas; las del usuario actual se destacan en la plantilla
    recetas = Receta.objects.all().select_related('user')
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas, 'user': request.user})


@login_required
def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear la receta sin guardar aún
            receta = form.save(commit=False)
            # Asignar el usuario actual como propietario
            receta.user = request.user
            receta.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm()
    return render(request, 'recetas/crear_receta.html', {'form': form})


@login_required
def borrar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
    # Solo el autor puede borrar su receta
    if receta.user != request.user:
        return HttpResponseForbidden('No tienes permiso para borrar esta receta')
    receta.delete()
    return redirect('lista_recetas')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_recetas')
    else:
        form = UserCreationForm()
    return render(request, 'recetas/register.html', {'form': form})


def inicio(request):
    """Página de inicio con enlaces a login/register y a la lista de recetas."""
    return render(request, 'recetas/inicio.html')


def logout_view(request):
    """Cerrar la sesión y redirigir a la lista de recetas."""
    auth_logout(request)
    return redirect('inicio')


@login_required
def editar_receta(request, id):
    """Editar una receta existente."""
    receta = get_object_or_404(Receta, id=id)
    # Verificar que el usuario actual es el autor
    if receta.user != request.user:
        return HttpResponseForbidden('No tienes permiso para editar esta receta')

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            # Guardar sin commit primero
            receta = form.save(commit=False)
            # Asegurar que el propietario no cambie
            receta.user = receta.user
            receta.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'recetas/crear_receta.html', {'form': form, 'receta': receta})


@login_required
def mi_perfil(request):
    """Vista de perfil del usuario: nombre, cantidad y listado de sus recetas propias."""
    user = request.user
    # Obtener solo las recetas del usuario actual
    recetas = Receta.objects.filter(user=user)
    # Contar el total de recetas del usuario
    total = recetas.count()
    return render(request, 'recetas/mi_perfil.html', {'perfil_user': user, 'recetas': recetas, 'total': total})
