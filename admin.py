import sqlite3
from pathlib import Path
from datetime import datetime
from getpass import getpass

from werkzeug.security import generate_password_hash


ARCHIVO_BD = Path("sistema.db")


def conectar():
    return sqlite3.connect(ARCHIVO_BD)


def crear_tabla_usuarios_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


def agregar_columna_rol_si_no_existe():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("PRAGMA table_info(usuarios)")
    columnas = cursor.fetchall()

    nombres_columnas = [columna[1] for columna in columnas]

    if "rol" not in nombres_columnas:
        cursor.execute("""
            ALTER TABLE usuarios
            ADD COLUMN rol TEXT NOT NULL DEFAULT 'usuario'
        """)

        print("Columna 'rol' agregada correctamente.")
    else:
        print("La columna 'rol' ya existe.")

    conexion.commit()
    conexion.close()


def buscar_usuario(correo):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, correo, rol
        FROM usuarios
        WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()

    conexion.close()

    return usuario


def crear_o_actualizar_admin(nombre, correo, password):
    password_hash = generate_password_hash(password)
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    usuario_existente = buscar_usuario(correo)

    conexion = conectar()
    cursor = conexion.cursor()

    if usuario_existente:
        cursor.execute("""
            UPDATE usuarios
            SET nombre = ?, password_hash = ?, rol = 'admin'
            WHERE correo = ?
        """, (nombre, password_hash, correo))

        print("Usuario existente actualizado como ADMIN.")
    else:
        cursor.execute("""
            INSERT INTO usuarios (nombre, correo, password_hash, fecha_registro, rol)
            VALUES (?, ?, ?, ?, 'admin')
        """, (nombre, correo, password_hash, fecha_registro))

        print("Usuario ADMIN creado correctamente.")

    conexion.commit()
    conexion.close()


def main():
    print("----- CREAR USUARIO ADMIN -----")

    crear_tabla_usuarios_si_no_existe()
    agregar_columna_rol_si_no_existe()

    nombre = input("Nombre del administrador: ").strip().title()
    correo = input("Correo del administrador: ").strip().lower()
    password = getpass("Contraseña del administrador: ")
    confirmar = getpass("Confirmar contraseña: ")

    if not nombre or not correo or not password or not confirmar:
        print("Error: todos los campos son obligatorios.")
        return

    if "@" not in correo:
        print("Error: escribe un correo válido.")
        return

    if len(password) < 6:
        print("Error: la contraseña debe tener mínimo 6 caracteres.")
        return

    if password != confirmar:
        print("Error: las contraseñas no coinciden.")
        return

    crear_o_actualizar_admin(nombre, correo, password)

    print("Listo. Ya puedes iniciar sesión como administrador.")


if __name__ == "__main__":
    main()