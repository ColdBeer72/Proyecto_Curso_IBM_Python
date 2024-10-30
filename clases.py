class Producto:
    """
    Clase que representa un producto en el inventario.

    Atributos:
        nombre (str): El nombre del producto.
        categoria (str): La categoría del producto.
        precio (float): El precio del producto (debe ser mayor a 0).
        cantidad (int): La cantidad de producto en stock (debe ser >= 0).
    """

    def __init__(self, nombre, categoria, precio, cantidad):
        self.set_nombre(nombre)
        self.set_categoria(categoria)
        self.set_precio(precio)
        self.set_cantidad(cantidad)

    def get_nombre(self):
        """Devuelve el nombre del producto."""
        return self.__nombre

    def set_nombre(self, nombre):
        """Establece el nombre del producto, lanzando un error si es vacío."""
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        self.__nombre = nombre

    def get_categoria(self):
        """Devuelve la categoría del producto."""
        return self.__categoria

    def set_categoria(self, categoria):
        """Establece la categoría del producto."""
        if not categoria:
            raise ValueError("La categoría no puede estar vacía")
        self.__categoria = categoria

    def get_precio(self):
        """Devuelve el precio del producto."""
        return self.__precio

    def set_precio(self, precio):
        """Establece el precio del producto, asegurando que sea mayor que 0."""
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        self.__precio = precio

    def get_cantidad(self):
        """Devuelve la cantidad del producto en stock."""
        return self.__cantidad

    def set_cantidad(self, cantidad):
        """Establece la cantidad de producto en stock, asegurando que sea >= 0."""
        if cantidad < 0:
            raise ValueError("La cantidad debe ser mayor o igual que 0")
        self.__cantidad = cantidad

    def to_dict(self):
        """Devuelve el producto en formato de diccionario."""
        return {
            "nombre": self.get_nombre(),
            "categoria": self.get_categoria(),
            "precio": self.get_precio(),
            "cantidad": self.get_cantidad()
        }

class Inventario:
    """
    Clase que representa un inventario de productos.

    Métodos:
        agregar_producto: Añade un nuevo producto al inventario.
        actualizar_producto: Actualiza precio o cantidad de un producto existente.
        eliminar_producto: Elimina un producto del inventario.
        mostrar_inventario: Lista todos los productos en el inventario.
        buscar_producto: Busca un producto por nombre.
    """

    def __init__(self):
        self.__productos = []

    def agregar_producto(self, producto):
        """Agrega un nuevo producto al inventario si no existe ya en la lista."""
        if any(p.get_nombre() == producto.get_nombre() for p in self.__productos):
            raise ValueError("El producto ya existe en el inventario")
        self.__productos.append(producto)
        return "Producto agregado exitosamente"

    def actualizar_producto(self, nombre, nuevo_precio=None, nueva_cantidad=None):
        """Actualiza el precio o cantidad en stock de un producto existente en el inventario."""
        producto = next((p for p in self.__productos if p.get_nombre() == nombre), None)
        if not producto:
            raise ValueError("Producto no encontrado")

        if nuevo_precio is not None:
            producto.set_precio(nuevo_precio)
        if nueva_cantidad is not None:
            producto.set_cantidad(nueva_cantidad)

        return "Producto actualizado exitosamente"

    def eliminar_producto(self, nombre):
        """Elimina un producto del inventario si existe."""
        producto = next((p for p in self.__productos if p.get_nombre() == nombre), None)
        if not producto:
            return "Producto no encontrado"
        self.__productos.remove(producto)
        return "Producto eliminado exitosamente"

    def mostrar_inventario(self):
        """Devuelve una lista de todos los productos en formato diccionario."""
        return [producto.to_dict() for producto in self.__productos]

    def buscar_producto(self, nombre):
        """Devuelve el producto que coincida con el nombre proporcionado."""
        for producto in self.__productos:
            if producto.get_nombre() == nombre:
                return producto.to_dict()
        return None
