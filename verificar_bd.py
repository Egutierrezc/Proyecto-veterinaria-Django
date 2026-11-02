"""
Script para verificar la conexion a MySQL y mostrar las tablas y datos
de la base de datos 'veterinaria'.

Uso:
    python verificar_bd.py
"""

import MySQLdb

HOST = '127.0.0.1'
USER = 'root'
PASSWORD = ''
DATABASE = 'veterinaria'
PORT = 3306


def main():
    try:
        conn = MySQLdb.connect(
            host=HOST,
            user=USER,
            passwd=PASSWORD,
            db=DATABASE,
            port=PORT,
        )
        cur = conn.cursor()

        print(f'Conexion exitosa a MySQL: {HOST}:{PORT} / {DATABASE}')
        print()

        print('Tablas en la base de datos:')
        cur.execute('SHOW TABLES')
        tablas = cur.fetchall()
        if not tablas:
            print('  (no hay tablas)')
        for t in tablas:
            print(f'  - {t[0]}')
        print()

        print('Mascotas registradas:')
        cur.execute(
            'SELECT id, nombre, especie, propietario, correo '
            'FROM mascotas_mascota ORDER BY id'
        )
        mascotas = cur.fetchall()
        if not mascotas:
            print('  (no hay mascotas registradas)')
        for m in mascotas:
            print(f'  {m[0]}. {m[1]} ({m[2]}) - dueno: {m[3]} - correo: {m[4]}')
        print()

        print(f'Total de mascotas: {len(mascotas)}')

        cur.close()
        conn.close()
        print()
        print('Verificacion completada correctamente.')

    except MySQLdb.Error as e:
        print(f'Error al conectar con MySQL: {e}')
        print()
        print('Revisa que:')
        print('  - XAMPP tenga MySQL corriendo (en verde).')
        print('  - La base de datos "veterinaria" exista.')
        print('  - El usuario root no tenga contrasena o ajusta PASSWORD.')


if __name__ == '__main__':
    main()