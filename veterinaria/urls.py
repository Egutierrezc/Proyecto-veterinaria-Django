from django.contrib import admin
from django.urls import include, path

from mascotas import views as mascotas_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', mascotas_views.login_view, name='login'),
    path('logout/', mascotas_views.logout_view, name='logout'),
    path('', include('mascotas.urls')),
]
