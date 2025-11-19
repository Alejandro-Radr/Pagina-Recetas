from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout

from .models import Receta
from .forms import RecetaForm


def lista_recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'recetas/lista_recetas.html', {'recetas': recetas})


@login_required
def crear_receta(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm()
    return render(request, 'recetas/crear_receta.html', {'form': form})


@login_required
def borrar_receta(request, id):
    receta = get_object_or_404(Receta, id=id)
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
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            return redirect('lista_recetas')
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'recetas/crear_receta.html', {'form': form, 'receta': receta})
