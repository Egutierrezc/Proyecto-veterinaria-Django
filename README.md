# Proyecto de veterinaria

Aplicación web para registrar y administrar mascotas.

## Para iniciar

1. Iniciar MySQL en XAMPP y crear la base `veterinaria` en phpMyAdmin.
2. Abrir PowerShell en la carpeta del proyecto y ejecutar:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:USE_MYSQL = "1"
$env:DB_NAME = "veterinaria"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
python manage.py migrate
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/`. Si `root` tiene contraseña(para mas adelante), cambiar el valor de `DB_PASSWORD`. Ejecutar todo desde la misma ventana de PowerShell.

## Inicio de sesión y token

El acceso a las vistas de mascotas requiere una cuenta de Django. El formulario de creación de cuentas queda fuera de este cambio; un administrador puede crear usuarios desde `/admin/`.

1. Iniciar sesión en `/login/` con el nombre de usuario y contraseña de Django.
2. Al iniciar sesión se muestra un token de autenticación. Guárdalo de forma segura; cerrar sesión lo invalida.
3. Las futuras solicitudes a endpoints REST protegidos deben incluir la cabecera `Authorization: Token <token>`.

La autenticación y los permisos por token de Django REST Framework están configurados. Los endpoints REST (GET, POST, PUT y DELETE) no forman parte de esta implementación de login y deberán agregarse por separado.
