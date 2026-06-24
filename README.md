Sistema Web de Ventas con Login en Python

Este proyecto es una aplicación web local desarrollada con Python, Flask, SQLite, Pandas y OpenPyXL.

El sistema permite registrar usuarios, iniciar sesión, registrar ventas, consultar el historial de ventas y descargar un reporte Excel. Cada usuario solo puede ver y administrar sus propias ventas.

Funciones principales

- Registro de usuarios desde una página web.
- Inicio de sesión con correo y contraseña.
- Protección de panel privado mediante sesión.
- Registro de ventas por usuario.
- Cálculo automático de subtotal, IVA y total.
- Visualización de resumen general de ventas.
- Historial de ventas en tabla.
- Eliminación de ventas registradas.
- Descarga de reporte Excel.
- Separación de información por usuario.
- Base de datos local con SQLite.
- Contraseñas protegidas mediante hash.

Tecnologías utilizadas

- Python
- Flask
- SQLite
- Pandas
- OpenPyXL
- HTML
- CSS
- Werkzeug Security

Estructura del proyecto

web_ventas_login/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── templates/
    ├── inicio.html
    ├── registro.html
    ├── login.html
    ├── panel.html
    └── reporte.html

Archivos principales

- "app.py": archivo principal de la aplicación.
- "templates/inicio.html": página principal del sistema.
- "templates/registro.html": formulario para crear usuarios.
- "templates/login.html": formulario para iniciar sesión.
- "templates/panel.html": panel privado para registrar y consultar ventas.
- "templates/reporte.html": archivo preparado para futuras mejoras.
- "requirements.txt": lista de librerías necesarias.
- ".gitignore": evita subir archivos generados o innecesarios.

Archivos generados automáticamente

Estos archivos se crean al usar el sistema y no deben subirse a GitHub:

- "sistema.db": base de datos SQLite donde se guardan usuarios y ventas.
- "reportes/": carpeta donde se generan los reportes Excel.
- "__pycache__/": archivos internos generados por Python.

Instalación

Instalar las librerías necesarias:

python -m pip install -r requirements.txt

Ejecución del proyecto

Ejecutar la aplicación con:

python app.py

Después abrir en el navegador:

http://127.0.0.1:5000

Uso del sistema

1. Crear una cuenta nueva.
2. Iniciar sesión con correo y contraseña.
3. Entrar al panel privado.
4. Registrar ventas con producto, cantidad y precio.
5. Consultar el resumen de ventas.
6. Revisar el historial de ventas registradas.
7. Eliminar ventas si es necesario.
8. Descargar el reporte Excel.
9. Cerrar sesión.

Reporte Excel

El sistema permite descargar un reporte Excel con la información del usuario que inició sesión.

El reporte incluye:

- Resumen general.
- Lista completa de ventas.
- Ventas agrupadas por producto.
- Ventas agrupadas por día.

Seguridad básica

Las contraseñas no se guardan en texto normal. El sistema utiliza hash de contraseñas mediante Werkzeug Security.

Además, cada usuario solo puede ver sus propias ventas, ya que las ventas se relacionan con el ID del usuario que inició sesión.

Objetivo del proyecto

El objetivo de este proyecto es practicar el desarrollo de una aplicación web funcional con Python, integrando usuarios, login, sesiones, base de datos, registro de información y generación de reportes Excel.

Este proyecto representa una base para sistemas más completos como puntos de venta, control de inventario, administración de clientes o paneles administrativos.