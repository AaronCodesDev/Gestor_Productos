from tkinter import ttk
from tkinter import *
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definiendo la direccion SQLite
DATABASE_URL = 'sqlite:///database/productos.db'

# Definiendo la base
Base = declarative_base()

# Definiendo Producto model
class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    subcategoria = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    outlet = Column(Boolean, default=False)

# Creando database engine
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Crear la tabla si no existe

# Creando session
Session = sessionmaker(bind=engine)
session = Session()

class ProductoApp:
    def __init__(self, root):
        self.ventana = root
        self.ventana.title('Gestor de Productos')
        self.ventana.resizable(1, 1)
        self.ventana.wm_iconbitmap('assets/icon.ico')

        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto', labelanchor='n')
        frame.grid(row=0, column=0, columnspan=4, pady=60)

        # Iniciando Labels y Entries
        self.etiqueta_nombre = Label(frame, text='Nombre: ')
        self.etiqueta_nombre.grid(row=1, column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        self.etiqueta_precio = Label(frame, text='Precio: ')
        self.etiqueta_precio.grid(row=2, column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        self.etiqueta_combo = Label(frame, text='Categoría: ')
        self.etiqueta_combo.grid(row=3, column=0)
        self.combo = ttk.Combobox(frame, state='readonly',
                                  values=['Componentes', 'Periféricos', 'Software', 'Accesorios', 'Servicios', 'Otros'], width=20)
        self.combo.grid(row=3, column=1, sticky='w')
        self.combo.set("Seleccione categoría")
        self.combo.config(foreground="grey")

        # Botón "Cargar" ahora está justo debajo de la categoría seleccionada
        self.boton_cargar = ttk.Button(frame, text='Cargar Sub Categorias', command=self.cambiar)
        self.boton_cargar.grid(row=4, column=1, padx=10)  # Se coloca al lado del combobox de categorías

        self.etiqueta_combo2 = Label(frame, text='Sub-Categoría: ')
        self.etiqueta_combo2.grid(row=5, column=0)
        self.combo2 = ttk.Combobox(frame, state='readonly', width=20)
        self.combo2.grid(row=5, column=1, sticky='w')
        self.combo2.set("Seleccione sub-categoría")
        self.combo2.config(foreground="grey")

        self.etiqueta_stock = Label(frame, text='Stock: ')
        self.etiqueta_stock.grid(row=6, column=0)
        self.stock = Entry(frame)
        self.stock.grid(row=6, column=1)

        self.etiqueta_outlet = Label(frame, text='Outlet: ')
        self.etiqueta_outlet.grid(row=7, column=0)
        self.outlet_value = BooleanVar()
        self.outlet = ttk.Checkbutton(frame, text="En oferta", variable=self.outlet_value)
        self.outlet.grid(row=7, column=1)

        self.boton_anadir = ttk.Button(frame, text='Guardar Producto', command=self.add_producto)
        self.boton_anadir.grid(row=8, columnspan=2, sticky=W + E, pady=10)

        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W + E)

        self.tabla = ttk.Treeview(height=20, columns=('Categoria', 'Sub-Categoria', 'Stock', 'Precio', 'Outlet'), style="mystyle.Treeview")
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('#1', text='Categoria', anchor=CENTER)
        self.tabla.heading('#2', text='Sub-Categoria', anchor=CENTER)
        self.tabla.heading('#3', text='Stock', anchor=CENTER)
        self.tabla.heading('#4', text='Precio', anchor=CENTER)
        self.tabla.heading('#5', text='Outlet', anchor=CENTER)

        # Alineado columnas
        self.tabla.column('#0', anchor=E)
        self.tabla.column('#1', anchor=CENTER)
        self.tabla.column('#2', anchor=CENTER)
        self.tabla.column('#3', anchor=CENTER)
        self.tabla.column('#4', anchor=E)
        self.tabla.column('#5', anchor=CENTER)

        boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto)
        boton_eliminar.grid(row=5, column=0, sticky=W + E)
        boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto)
        boton_editar.grid(row=5, column=1, sticky=W + E)

        self.get_productos()

    def cambiar(self):
        categoria = self.combo.get()
        if categoria == 'Componentes':
            self.combo2['values'] = ('Procesadores', 'Tarjetas graficas', 'Memoria RAM', 'Almacenamiento', 'Fuentes de alimentacion', 'Refrigeración', 'Otros')
        elif categoria == 'Periféricos':
            self.combo2['values'] = ('Teclados', 'Ratones', 'Monitores', 'Impresoras', 'Escáneres', 'Dispositivos de entrada/salida')
        elif categoria == 'Software':
            self.combo2['values'] = ('Sistemas operativos', 'Aplicaciones de software', 'Juegos')
        elif categoria == 'Accesorios':
            self.combo2['values'] = ('Fundas y maletines', 'Cables y adaptadores')
        elif categoria == 'Servicios':
            self.combo2['values'] = ('Reparación y mantenimiento', 'Asesoramiento técnico', 'Instalación de software y sistemas operativos')
        elif categoria == 'Otros':
            self.combo2['values'] = ('Otros')

    def get_productos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = session.query(Producto).order_by(Producto.nombre.desc()).all()

        for producto in productos:
            outlet_info = "Activo" if producto.outlet else ''
            precio_formateado = '{:.2f} €'.format(producto.precio)
            self.tabla.insert('', 0, text=producto.nombre,
                              values=(producto.categoria, producto.subcategoria, producto.stock, precio_formateado, outlet_info))

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0

    def validacion_precio(self):
        return len(self.precio.get()) != 0

    def validacion_combo(self):
        return len(self.combo.get()) != 0

    def validacion_subcategoria(self):
        return len(self.combo2.get()) !=0

    def validacion_stock(self):
        return len(self.stock.get()) != 0

    def add_producto(self):
        if self.validacion_nombre() and self.validacion_precio() and self.validacion_combo() and self.validacion_subcategoria() and self.validacion_stock():
            precio_str = self.precio.get().replace(',', '.')
            nuevo_producto = Producto(
                nombre=self.nombre.get(),
                precio=float(precio_str),
                categoria=self.combo.get(),
                subcategoria=self.combo2.get(),
                stock=int(self.stock.get()),
                outlet=self.outlet_value.get()
            )
            session.add(nuevo_producto)
            session.commit()
            self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito'

            # Limpiar los campos
            self.nombre.delete(0, END)
            self.precio.delete(0, END)
            self.combo.set('Seleccione categoría')
            self.combo2.set('Seleccione sub-categoría')
            self.stock.delete(0, END)
            self.outlet_value.set(False)

            self.get_productos()
        else:
            self.mensaje['text'] = 'Todos los campos son obligatorios'

    def del_producto(self):
        nombre = self.tabla.item(self.tabla.selection())['text']
        producto = session.query(Producto).filter_by(nombre=nombre).first()
        if producto:
            session.delete(producto)
            session.commit()
            self.mensaje['text'] = f'Producto {nombre} eliminado con éxito'
            self.get_productos()

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            old_nombre = self.tabla.item(self.tabla.selection())['text']
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        producto = session.query(Producto).filter_by(nombre=old_nombre).first()

        self.ventana_editar = Toplevel()
        self.ventana_editar.title('Editar Producto')
        self.ventana_editar.resizable(1, 1)

        frame_editar = LabelFrame(self.ventana_editar, text='Editar el siguiente Producto', labelanchor='n')
        frame_editar.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        # Nombre
        Label(frame_editar, text='Nombre: ').grid(row=1, column=0, sticky=W)
        nuevo_nombre = Entry(frame_editar)
        nuevo_nombre.grid(row=1, column=1)
        nuevo_nombre.insert(0, producto.nombre)

        # Precio
        Label(frame_editar, text='Precio: ').grid(row=2, column=0, sticky=W)
        nuevo_precio = Entry(frame_editar)
        nuevo_precio.grid(row=2, column=1)
        nuevo_precio.insert(0, producto.precio)

        # Categoría
        Label(frame_editar, text='Categoría: ').grid(row=3, column=0, sticky=W)
        nuevo_combo = ttk.Combobox(frame_editar, state='readonly',
                                   values=['Componentes', 'Periféricos', 'Software', 'Accesorios', 'Servicios',
                                           'Otros'])
        nuevo_combo.grid(row=3, column=1)
        nuevo_combo.set(producto.categoria if producto.categoria else "Seleccione categoría")

        # Botón para cargar sub-categorías
        boton_cargar = ttk.Button(frame_editar, text='Cargar Sub-Categorías',
                                  command=lambda: self.cargar_subcategorias(nuevo_combo, nuevo_combo2))
        boton_cargar.grid(row=4, column=1, pady=5)

        # Sub-Categoría
        Label(frame_editar, text='Sub-Categoría: ').grid(row=5, column=0, sticky=W)
        nuevo_combo2 = ttk.Combobox(frame_editar, state='readonly')
        nuevo_combo2.grid(row=5, column=1)
        # Manejo seguro de la subcategoría
        if hasattr(producto, 'subcategoria') and producto.subcategoria:
            nuevo_combo2.set(producto.subcategoria)
        else:
            nuevo_combo2.set("Seleccione sub-categoría")

        # Stock
        Label(frame_editar, text='Stock: ').grid(row=6, column=0, sticky=W)
        nuevo_stock = Entry(frame_editar)
        nuevo_stock.grid(row=6, column=1)
        nuevo_stock.insert(0, producto.stock)

        # Outlet
        Label(frame_editar, text='Outlet: ').grid(row=7, column=0, sticky=W)
        nuevo_outlet_value = BooleanVar(value=producto.outlet)
        nuevo_outlet = ttk.Checkbutton(frame_editar, text="En oferta", variable=nuevo_outlet_value)
        nuevo_outlet.grid(row=7, column=1)

        # Botón para actualizar el producto
        ttk.Button(frame_editar, text='Actualizar',
                   command=lambda: self.actualizar_producto(
                       nuevo_nombre.get(), nuevo_precio.get(), nuevo_combo.get(),
                       nuevo_combo2.get(), nuevo_stock.get(), nuevo_outlet_value.get(), producto)
                   ).grid(row=8, column=0, columnspan=2, sticky=W + E, pady=10)

        self.ventana_editar.grab_set()  # Hace que la ventana de edición sea modal


    def cargar_subcategorias(self, combo_categoria, combo_subcategoria):
        """Esta función se encarga de actualizar las subcategorías según la categoría seleccionada."""
        categoria = combo_categoria.get()
        if categoria == 'Componentes':
            combo_subcategoria['values'] = (
            'Procesadores', 'Tarjetas graficas', 'Memoria RAM', 'Almacenamiento', 'Fuentes de alimentacion',
            'Refrigeración', 'Otros')
        elif categoria == 'Periféricos':
            combo_subcategoria['values'] = (
            'Teclados', 'Ratones', 'Monitores', 'Impresoras', 'Escáneres', 'Dispositivos de entrada/salida')
        elif categoria == 'Software':
            combo_subcategoria['values'] = ('Sistemas operativos', 'Aplicaciones de software', 'Juegos')
        elif categoria == 'Accesorios':
            combo_subcategoria['values'] = ('Fundas y maletines', 'Cables y adaptadores')
        elif categoria == 'Servicios':
            combo_subcategoria['values'] = (
            'Reparación y mantenimiento', 'Asesoramiento técnico', 'Instalación de software y sistemas operativos')
        elif categoria == 'Otros':
            combo_subcategoria['values'] = ('Otros')

    def actualizar_producto(self, nuevo_nombre, nuevo_precio, nueva_categoria, nueva_subcategoria, nuevo_stock, nuevo_outlet, producto):
        producto.nombre = nuevo_nombre
        producto.precio = float(nuevo_precio)
        producto.categoria = nueva_categoria
        producto.subcategoria = nueva_subcategoria
        producto.stock = int(nuevo_stock)
        producto.outlet = nuevo_outlet

        session.commit()
        self.ventana_editar.destroy()
        self.mensaje['text'] = f'Producto {producto.nombre} actualizado con éxito'
        self.get_productos()

if __name__ == '__main__':
    root = Tk()
    app = ProductoApp(root)
    root.mainloop()