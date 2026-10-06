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
