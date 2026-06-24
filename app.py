import sqlite3
from pathlib import Path
from datetime import datetime
from functools import wraps

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment


app = Flask(__name__)

app.secret_key = "clave_secreta_solo_para_pruebas"

ARCHIVO_BD = Path("sistema.db")
CARPETA_REPORTES = Path("reportes")
CARPETA_REPORTES.mkdir(exist_ok=True)


def conectar():
    return sqlite3.connect(ARCHIVO_BD)


def crear_tablas():
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

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            subtotal REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    """)

    conexion.commit()
    conexion.close()


def login_requerido(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return funcion(*args, **kwargs)

    return envoltura


def buscar_usuario_por_correo(correo):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, correo, password_hash
        FROM usuarios
        WHERE correo = ?
    """, (correo,))

    usuario = cursor.fetchone()
    conexion.close()

    return usuario


def buscar_usuario_por_id(usuario_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, nombre, correo, fecha_registro
        FROM usuarios
        WHERE id = ?
    """, (usuario_id,))

    usuario = cursor.fetchone()
    conexion.close()

    return usuario


def registrar_venta(usuario_id, producto, cantidad, precio):
    producto = producto.strip().title()
    cantidad = int(cantidad)
    precio = float(precio)

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    subtotal = cantidad * precio
    iva = subtotal * 0.16
    total = subtotal + iva

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO ventas (
            usuario_id, fecha, hora, producto, cantidad, precio, subtotal, iva, total
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        fecha,
        hora,
        producto,
        cantidad,
        precio,
        subtotal,
        iva,
        total
    ))

    conexion.commit()
    conexion.close()


def obtener_ventas_usuario(usuario_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, fecha, hora, producto, cantidad, precio, subtotal, iva, total
        FROM ventas
        WHERE usuario_id = ?
        ORDER BY id DESC
    """, (usuario_id,))

    ventas = cursor.fetchall()
    conexion.close()

    return ventas


def obtener_resumen_usuario(usuario_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(cantidad), 0),
            COALESCE(SUM(subtotal), 0),
            COALESCE(SUM(iva), 0),
            COALESCE(SUM(total), 0)
        FROM ventas
        WHERE usuario_id = ?
    """, (usuario_id,))

    resultado = cursor.fetchone()
    conexion.close()

    ventas_registradas, cantidad_total, subtotal, iva, total = resultado

    return {
        "ventas_registradas": ventas_registradas,
        "cantidad_total": cantidad_total,
        "subtotal": subtotal,
        "iva": iva,
        "total": total
    }


def eliminar_venta(usuario_id, venta_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM ventas
        WHERE id = ? AND usuario_id = ?
    """, (venta_id, usuario_id))

    conexion.commit()
    conexion.close()


def crear_reporte_excel(usuario_id):
    conexion = conectar()

    ventas = pd.read_sql_query("""
        SELECT id, fecha, hora, producto, cantidad, precio, subtotal, iva, total
        FROM ventas
        WHERE usuario_id = ?
        ORDER BY id
    """, conexion, params=(usuario_id,))

    conexion.close()

    if ventas.empty:
        raise ValueError("No hay ventas registradas para generar el reporte.")

    resumen = pd.DataFrame({
        "Dato": [
            "Ventas registradas",
            "Cantidad total vendida",
            "Subtotal general",
            "IVA general",
            "Total vendido"
        ],
        "Valor": [
            len(ventas),
            ventas["cantidad"].sum(),
            ventas["subtotal"].sum(),
            ventas["iva"].sum(),
            ventas["total"].sum()
        ]
    })

    ventas_por_producto = (
        ventas.groupby("producto", as_index=False)
        .agg({
            "cantidad": "sum",
            "subtotal": "sum",
            "iva": "sum",
            "total": "sum"
        })
        .sort_values("total", ascending=False)
    )

    ventas_por_dia = (
        ventas.groupby("fecha", as_index=False)
        .agg({
            "cantidad": "sum",
            "subtotal": "sum",
            "iva": "sum",
            "total": "sum"
        })
        .sort_values("fecha")
    )

    fecha_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta_reporte = CARPETA_REPORTES / f"reporte_usuario_{usuario_id}_{fecha_archivo}.xlsx"

    with pd.ExcelWriter(ruta_reporte, engine="openpyxl") as writer:
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
        ventas.to_excel(writer, sheet_name="Ventas", index=False)
        ventas_por_producto.to_excel(writer, sheet_name="Ventas por producto", index=False)
        ventas_por_dia.to_excel(writer, sheet_name="Ventas por dia", index=False)

    dar_formato_excel(ruta_reporte)

    return ruta_reporte


def dar_formato_excel(ruta_reporte):
    libro = load_workbook(ruta_reporte)

    for hoja in libro.worksheets:
        hoja.freeze_panes = "A2"

        for celda in hoja[1]:
            celda.font = Font(bold=True)
            celda.alignment = Alignment(horizontal="center")

        for columna in hoja.columns:
            ancho_maximo = 0
            letra = columna[0].column_letter

            for celda in columna:
                if celda.value is not None:
                    ancho_maximo = max(ancho_maximo, len(str(celda.value)))

                encabezado = hoja.cell(row=1, column=celda.column).value

                if encabezado in ["precio", "subtotal", "iva", "total", "Valor"]:
                    if isinstance(celda.value, (int, float)):
                        celda.number_format = '$#,##0.00'

            hoja.column_dimensions[letra].width = ancho_maximo + 8

    libro.save(ruta_reporte)


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    error = None
    mensaje = None

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip().title()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        confirmar = request.form.get("confirmar", "")

        try:
            if not nombre or not correo or not password or not confirmar:
                raise ValueError("Completa todos los campos.")

            if "@" not in correo:
                raise ValueError("Escribe un correo válido.")

            if len(password) < 6:
                raise ValueError("La contraseña debe tener mínimo 6 caracteres.")

            if password != confirmar:
                raise ValueError("Las contraseñas no coinciden.")

            usuario_existente = buscar_usuario_por_correo(correo)

            if usuario_existente:
                raise ValueError("Ese correo ya está registrado.")

            password_hash = generate_password_hash(password)
            fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, password_hash, fecha_registro)
                VALUES (?, ?, ?, ?)
            """, (nombre, correo, password_hash, fecha_registro))

            conexion.commit()
            conexion.close()

            mensaje = "Usuario registrado correctamente. Ahora puedes iniciar sesión."

        except ValueError as problema:
            error = str(problema)

    return render_template("registro.html", error=error, mensaje=mensaje)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")

        usuario = buscar_usuario_por_correo(correo)

        if not usuario:
            error = "Correo o contraseña incorrectos."
        else:
            usuario_id, nombre, correo_bd, password_hash = usuario

            if check_password_hash(password_hash, password):
                session["usuario_id"] = usuario_id
                session["usuario_nombre"] = nombre
                return redirect(url_for("panel"))

            error = "Correo o contraseña incorrectos."

    return render_template("login.html", error=error)


@app.route("/panel", methods=["GET", "POST"])
@login_requerido
def panel():
    error = None
    mensaje = None

    usuario_id = session["usuario_id"]
    usuario = buscar_usuario_por_id(usuario_id)

    if request.method == "POST":
        producto = request.form.get("producto", "")
        cantidad = request.form.get("cantidad", "")
        precio = request.form.get("precio", "")

        try:
            if not producto or not cantidad or not precio:
                raise ValueError("Completa producto, cantidad y precio.")

            if int(cantidad) <= 0:
                raise ValueError("La cantidad debe ser mayor a 0.")

            if float(precio) <= 0:
                raise ValueError("El precio debe ser mayor a 0.")

            registrar_venta(usuario_id, producto, cantidad, precio)
            mensaje = "Venta registrada correctamente."

        except ValueError as problema:
            error = str(problema)

    ventas = obtener_ventas_usuario(usuario_id)
    resumen = obtener_resumen_usuario(usuario_id)

    return render_template(
        "panel.html",
        usuario=usuario,
        ventas=ventas,
        resumen=resumen,
        error=error,
        mensaje=mensaje
    )


@app.route("/eliminar/<int:venta_id>")
@login_requerido
def eliminar(venta_id):
    usuario_id = session["usuario_id"]
    eliminar_venta(usuario_id, venta_id)

    return redirect(url_for("panel"))


@app.route("/descargar-reporte")
@login_requerido
def descargar_reporte():
    usuario_id = session["usuario_id"]

    try:
        ruta_reporte = crear_reporte_excel(usuario_id)

        return send_file(
            ruta_reporte,
            as_attachment=True,
            download_name=ruta_reporte.name
        )

    except Exception as error:
        usuario = buscar_usuario_por_id(usuario_id)
        ventas = obtener_ventas_usuario(usuario_id)
        resumen = obtener_resumen_usuario(usuario_id)

        return render_template(
            "panel.html",
            usuario=usuario,
            ventas=ventas,
            resumen=resumen,
            error=str(error),
            mensaje=None
        )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    crear_tablas()
    app.run(debug=True)