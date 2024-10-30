# /DEFINICIONES ARCHIVOS CASO PRÁCTICO EVALUABLE
# ├── app.py                 # Archivo principal para ejecutar Flask
# ├── clases.py              # Clases Producto e Inventario con documentación
# ├── templates/             # Directorio de plantillas HTML
# │   ├── base.html          # Plantilla base para herencia
# │   ├── index.html         # Página de inicio con el listado de productos
# │   ├── agregar.html       # Formulario para agregar un nuevo producto
# │   ├── actualizar.html    # Formulario para actualizar un producto
# │   └── eliminar.html      # Confirmación de eliminación de producto
# └── static/                # Directorio para archivos estáticos (CSS, JS)
#     └── style.css          # Estilos CSS para la aplicación web

import unicodedata
from flask import Flask, render_template, request, redirect, url_for, flash
from clases import Producto, Inventario

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave secreta para mensajes flash

# Crear instancia del inventario
inventario = Inventario()

# Agregar productos de ejemplo al inventario
productos_ejemplo = [
    Producto("Manzanas", "Frutas", 1.20, 150),
    Producto("Leche", "Lácteos", 0.90, 80),
    Producto("Arroz", "Cereales", 1.50, 200),
    Producto("Jabón Líquido", "Limpieza", 3.50, 60),
    Producto("Pasta Dental", "Higiene", 2.00, 90),
    Producto("Silla", "Muebles", 45.00, 30),
    Producto("Aceite de Oliva", "Aceites", 10.50, 40),
    Producto("Café", "Bebidas", 8.50, 50),
    Producto("Cereal de Maíz", "Cereales", 3.00, 70),
    Producto("Té Verde", "Bebidas", 5.00, 120),
    Producto("Shampoo", "Higiene", 4.00, 45),
    Producto("Monitor LED", "Electrónica", 120.00, 25),
    Producto("Cargador USB", "Electrónica", 8.00, 100),
    Producto("Plátanos", "Frutas", 1.10, 110),
    Producto("Queso Cheddar", "Lácteos", 3.50, 60),
    Producto("Detergente en Polvo", "Limpieza", 6.50, 40),
    Producto("Mesa de Centro", "Muebles", 80.00, 10),
    Producto("Mantequilla", "Lácteos", 2.50, 90),
    Producto("Jugo de Naranja", "Bebidas", 3.20, 75),
    Producto("Azúcar", "Condimentos", 1.00, 140),
]

# Añadir los productos de ejemplo al inventario
for producto in productos_ejemplo:
    inventario.agregar_producto(producto)

# Función para normalizar texto (eliminar acentos y convertir a minúsculas)
def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.lower()

@app.route('/')
def index():
    """Página de inicio que muestra todos los productos en el inventario."""
    productos = inventario.mostrar_inventario()
    return render_template('index.html', productos=productos)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar_producto():
    """Permite buscar un producto por su nombre, insensible a mayúsculas/minúsculas y acentos."""
    if request.method == 'POST':
        nombre_busqueda = request.form['nombre']
        nombre_normalizado = normalizar_texto(nombre_busqueda)
        
        # Buscar coincidencias parciales en nombres de productos
        productos_encontrados = [
            producto for producto in inventario.mostrar_inventario()
            if nombre_normalizado in normalizar_texto(producto['nombre'])
        ]
        
        if productos_encontrados:
            return render_template('index.html', productos=productos_encontrados, busqueda=True, nombre=nombre_busqueda)
        else:
            flash('Producto no encontrado')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    """Muestra el formulario para agregar un nuevo producto y procesa la solicitud POST para añadirlo."""
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        try:
            precio = float(request.form['precio'])
            cantidad = int(request.form['cantidad'])
            nuevo_producto = Producto(nombre, categoria, precio, cantidad)
            mensaje = inventario.agregar_producto(nuevo_producto)
            flash(mensaje)
            return redirect(url_for('index'))
        except ValueError as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('agregar_producto'))
    return render_template('agregar.html')

@app.route('/actualizar/<nombre>', methods=['GET', 'POST'])
def actualizar_producto(nombre):
    """Muestra el formulario para actualizar un producto y procesa la solicitud POST para realizar la actualización."""
    producto = inventario.buscar_producto(nombre)
    if not producto:
        flash('Producto no encontrado')
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            nuevo_precio = float(request.form['precio'])
            nueva_cantidad = int(request.form['cantidad'])
            mensaje = inventario.actualizar_producto(nombre, nuevo_precio, nueva_cantidad)
            flash(mensaje)
            return redirect(url_for('index'))
        except ValueError as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('actualizar_producto', nombre=nombre))
    return render_template('actualizar.html', producto=producto)

@app.route('/eliminar/<nombre>', methods=['GET', 'POST'])
def eliminar_producto(nombre):
    """Muestra la confirmación de eliminación de producto y procesa la solicitud POST para eliminar el producto."""
    if request.method == 'POST':
        mensaje = inventario.eliminar_producto(nombre)
        flash(mensaje)
        return redirect(url_for('index'))
    return render_template('eliminar.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
