from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from rest_framework.authtoken.models import Token

from .forms import MascotaForm
from .models import Mascota


def home(request):
    return render(request, 'mascotas/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.POST.get('next') or request.GET.get('next', '')
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = reverse('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            Token.objects.get_or_create(user=user)
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)

    form.fields['username'].widget.attrs.update({'class': 'form-control', 'autofocus': True})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})
    return render(request, 'registration/login.html', {'form': form, 'next': next_url})


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('home')


@login_required
def mascota_list(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotas/mascota_list.html', {'mascotas': mascotas})


@login_required
def mascota_create(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mascota_list')
    else:
        form = MascotaForm()

    return render(request, 'mascotas/mascota_form.html', {'form': form, 'titulo': 'Registrar mascota'})


@login_required
def mascota_update(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        form = MascotaForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            return redirect('mascota_list')
    else:
        form = MascotaForm(instance=mascota)

    return render(request, 'mascotas/mascota_form.html', {'form': form, 'titulo': 'Editar mascota', 'mascota': mascota})


@login_required
def mascota_delete(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota_list')

    return render(request, 'mascotas/mascota_confirm_delete.html', {'mascota': mascota})
