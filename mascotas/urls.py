from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mascotas/', views.mascota_list, name='mascota_list'),
    path('mascotas/nueva/', views.mascota_create, name='mascota_create'),
    path('mascotas/<int:pk>/editar/', views.mascota_update, name='mascota_update'),
    path('mascotas/<int:pk>/eliminar/', views.mascota_delete, name='mascota_delete'),
]
