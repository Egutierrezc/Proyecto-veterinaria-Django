# Ejecutar el proyecto

1. Inicia MySQL en XAMPP y crea una base de datos llamada `veterinaria` en phpMyAdmin.
2. Abre PowerShell en esta carpeta y ejecuta:

```powershell
py -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
$env:USE_MYSQL = "1"
$env:DB_NAME = "veterinaria"
$env:DB_USER = "root"
$env:DB_PASSWORD = ""
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py runserver
```

Abre `http://127.0.0.1:8000/` en el navegador. Si el usuario `root` de MySQL tiene contraseña, asígnala a `DB_PASSWORD`.
