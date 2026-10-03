# Veterinaria CRUD con Django

Este proyecto inicia la base para una aplicación web de veterinaria con Django.

## Parte 1: estructura base

- Proyecto Django: `veterinaria`
- Aplicación: `mascotas`
- Modelo inicial: `Mascota`
- Vistas CRUD básicas
- Templates con navegabilidad
- Validaciones de formulario

## Siguientes pasos

1. Crear y activar entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Ejecutar `python manage.py migrate`.
4. Crear superusuario opcional con `python manage.py createsuperuser`.
5. Configurar MySQL/MariaDB para producción.

## Configuración MySQL/MariaDB

La configuración actual usa SQLite por defecto para poder trabajar de manera local y rápida. Si quieres conectarte a MySQL, habilita la variable `USE_MYSQL=1` y define los datos de conexión en el entorno.

Ejemplo:

```bash
export USE_MYSQL=1
export DB_NAME=veterinaria
export DB_USER=root
export DB_PASSWORD=tu_password
export DB_HOST=localhost
export DB_PORT=3306
```

Luego ejecuta:

```bash
python manage.py migrate
```
