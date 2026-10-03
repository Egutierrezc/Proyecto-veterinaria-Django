from django.shortcuts import get_object_or_404, redirect, render

from .forms import MascotaForm
from .models import Mascota


def home(request):
    return render(request, 'mascotas/home.html')


def mascota_list(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotas/mascota_list.html', {'mascotas': mascotas})


def mascota_create(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mascota_list')
    else:
        form = MascotaForm()

    return render(request, 'mascotas/mascota_form.html', {'form': form, 'titulo': 'Registrar mascota'})


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


def mascota_delete(request, pk):
    mascota = get_object_or_404(Mascota, pk=pk)

    if request.method == 'POST':
        mascota.delete()
        return redirect('mascota_list')

    return render(request, 'mascotas/mascota_confirm_delete.html', {'mascota': mascota})
