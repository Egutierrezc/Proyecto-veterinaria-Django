@echo off
REM Script para levantar el servidor Django con MySQL activado.
REM Uso: haz doble clic sobre este archivo, o ejecutalo desde CMD.

echo Activando entorno virtual...
call venv\Scripts\activate

echo Configurando variables de entorno para MySQL...
set USE_MYSQL=1
set DB_HOST=127.0.0.1
set DB_NAME=veterinaria
set DB_USER=root
set DB_PORT=3306

echo.
echo Iniciando servidor Django en http://127.0.0.1:8000/
echo Presiona CTRL+C para detenerlo.
echo.

python manage.py runserver