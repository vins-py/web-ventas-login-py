Sistema Web de Ventas con Login, Administrador e Inventario

Este proyecto es una aplicación web local desarrollada con Python, Flask, SQLite, Pandas y OpenPyXL.

El sistema permite registrar usuarios, iniciar sesión, registrar ventas, administrar inventario, controlar stock automáticamente, consultar historial y descargar reportes Excel.

Cada usuario normal solo puede ver y administrar sus propias ventas. El administrador puede ver todos los usuarios, todas las ventas, administrar productos y descargar un reporte general.

Funciones principales

- Registro de usuarios desde una página web.
- Inicio de sesión con correo y contraseña.
- Protección de panel privado mediante sesión.
- Registro de ventas por usuario.
- Separación de información por usuario.
- Panel de administrador.
- Visualización de todos los usuarios registrados.
- Visualización de todas las ventas del sistema.
- Administración de inventario.
- Registro de productos con precio y stock.
- Descuento automático de stock al vender.
- Bloqueo de venta cuando no hay suficiente stock.
- Restauración de stock al eliminar una venta.
- Cálculo automático de subtotal, IVA y total.
- Descarga de reporte Excel individual.
- Descarga de reporte general Excel.
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
├── crear_admin.py
├── README.md
├── requirements.txt
├── .gitignore
└── templates/
    ├── inicio.html
    ├── registro.html
    ├── login.html
    ├── panel.html
    ├── admin.html
    ├── inventario.html
    └── reporte.html

Archivos principales

- "app.py": archivo principal de la aplicación.
- "crear_admin.py": permite crear o actualizar un usuario administrador.
- "templates/inicio.html": página principal del sistema.
- "templates/registro.html": formulario para crear usuarios.
- "templates/login.html": formulario para iniciar sesión.
- "templates/panel.html": panel privado para registrar y consultar ventas.
- "templates/admin.html": panel del administrador.
- "templates/inventario.html": pantalla para administrar productos y stock.
- "templates/reporte.html": archivo preparado para futuras mejoras.
- "requirements.txt": lista de librerías necesarias.
- ".gitignore": evita subir archivos generados o innecesarios.

Archivos generados automáticamente

Estos archivos se crean al usar el sistema y no deben subirse a GitHub:

- "sistema.db": base de datos SQLite donde se guardan usuarios, productos y ventas.
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

Crear usuario administrador

Antes de iniciar sesión como administrador, ejecutar:

python crear_admin.py

El programa pedirá:

Nombre del administrador
Correo del administrador
Contraseña del administrador
Confirmar contraseña

Después de crear el administrador, se puede iniciar sesión desde la página de login.

Uso del sistema como usuario normal

1. Crear una cuenta nueva.
2. Iniciar sesión con correo y contraseña.
3. Entrar al panel privado.
4. Seleccionar un producto disponible.
5. Registrar una venta con cantidad.
6. Consultar el resumen de ventas.
7. Revisar el historial de ventas registradas.
8. Eliminar ventas si es necesario.
9. Descargar el reporte Excel individual.
10. Cerrar sesión.

Uso del sistema como administrador

1. Ejecutar "crear_admin.py" para crear el usuario administrador.
2. Iniciar sesión con el correo y contraseña del administrador.
3. Entrar al panel de administrador.
4. Ver usuarios registrados.
5. Ver todas las ventas del sistema.
6. Entrar al módulo de inventario.
7. Registrar productos con precio y stock.
8. Ver productos disponibles, stock bajo o sin stock.
9. Descargar el reporte general Excel.
10. Cerrar sesión.

Inventario

El sistema cuenta con un módulo de inventario donde el administrador puede registrar productos.

Cada producto contiene:

- Nombre.
- Precio.
- Stock disponible.
- Fecha de registro.

Cuando un usuario registra una venta, el sistema descuenta automáticamente el stock del producto vendido.

Si el usuario intenta vender más piezas de las disponibles, el sistema no permite registrar la venta.

Cuando se elimina una venta, el sistema restaura el stock correspondiente.

Reportes Excel

El sistema permite generar dos tipos de reportes:

Reporte individual

Cada usuario puede descargar un reporte con sus propias ventas.

Incluye:

- Resumen general.
- Lista completa de ventas.
- Ventas agrupadas por producto.
- Ventas agrupadas por día.

Reporte general

El administrador puede descargar un reporte general de todo el sistema.

Incluye:

- Resumen general.
- Usuarios registrados.
- Inventario.
- Todas las ventas.
- Ventas agrupadas por usuario.
- Ventas agrupadas por producto.
- Ventas agrupadas por día.

Seguridad básica

Las contraseñas no se guardan en texto normal. El sistema utiliza hash de contraseñas mediante Werkzeug Security.

Cada usuario solo puede ver sus propias ventas, ya que las ventas se relacionan con el ID del usuario que inició sesión.

El panel de administrador está protegido mediante rol de usuario. Solo los usuarios con rol "admin" pueden entrar al panel administrativo y administrar inventario.

Objetivo del proyecto

El objetivo de este proyecto es practicar el desarrollo de una aplicación web funcional con Python, integrando usuarios, login, sesiones, roles, inventario, stock automático, base de datos, registro de ventas y generación de reportes Excel.

Este proyecto representa una base para sistemas más completos como puntos de venta, control de inventario, administración de clientes, paneles administrativos o sistemas internos para negocios.