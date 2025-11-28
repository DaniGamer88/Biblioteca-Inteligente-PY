# ======================================================================
#                    PROYECTO: BIBLIOTECA INTELIGENTE
#        Estructuras: Lista Ligada, Cola, Pila, Arbol, Grafo
#        Algoritmos: Burbuja, Busqueda Secuencial, Busqueda Binaria
# ======================================================================
# El sistema administra una biblioteca usando varias estructuras de datos
# fundamentales. Permite manejar libros, usuarios, prestamos, categorias
# y relaciones entre libros (grafo). Este archivo contiene el codigo
# completo y comentarios explicativos estilo B (tecnico y humano).
# ======================================================================

from dataclasses import dataclass, field
from typing import Optional, Any, List, Dict
import os
import pickle
from tabulate import tabulate
import tkinter as tk
from tkinter import scrolledtext

# ======================================================================
#region LISTA LIGADA
# ======================================================================
# Estructura para almacenar libros y usuarios. Permite crecimiento
# dinamico y operaciones basicas sin usar listas nativas directamente.
# Usamos esta estructura para mostrar que trabajamos con punteros/links.
# ======================================================================

@dataclass
class Node:
    # Nodo basico para la lista ligada: almacena 'data' y el puntero 'next'
    data: Any
    next: Optional['Node'] = None


class LinkedList:
# Funcion: __init__
    def __init__(self):
        # head apunta al primer nodo; si es None, la lista esta vacia
        self.head: Optional[Node] = None

# Funcion: append
    def append(self, data):
        # Inserta un nuevo nodo al final de la lista
        new_node = Node(data)

        if not self.head:
            # Si la lista esta vacia, el nuevo nodo es la cabeza
            self.head = new_node
            return

        # Si no, recorremos hasta el ultimo nodo y enlazamos
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

# Funcion: find
    def find(self, predicate) -> Optional[Any]:
        # Busca el primer elemento que cumpla la condicion 'predicate'
        # predicate es una funcion que toma data y devuelve True/False
        cur = self.head
        while cur:
            if predicate(cur.data):
                return cur.data
            cur = cur.next
        return None

# Funcion: remove
    def remove(self, predicate) -> bool:
        # Elimina el primer nodo que cumpla la condicion predicate
        prev = None
        cur = self.head
        while cur:
            if predicate(cur.data):
                # Si hay un anterior, saltarlo; si no, mover head
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

# Funcion: to_list
    def to_list(self) -> List[Any]:
        # Convierte la lista ligada a una lista de Python para operaciones
        result = []
        cur = self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

# Funcion: __iter__
    def __iter__(self):
        # Permite iterar la lista con 'for item in linkedlist'
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next


# ======================================================================
#region COLA (FIFO)
# ======================================================================
# Cola simple usando lista nativa. Se usa para solicitudes de prestamo
# porque el primer que llega es el primero que se atiende (FIFO).
# ======================================================================

class Queue:
# Funcion: __init__
    def __init__(self):
        # items guardara tuplas (user_id, isbn) para solicitudes
        self.items: List[Any] = []

# Funcion: enqueue
    def enqueue(self, item):
        # Agrega al final de la cola
        self.items.append(item)

# Funcion: dequeue
    def dequeue(self) -> Optional[Any]:
        # Retira y devuelve el primer elemento; si esta vacia devuelve None
        if not self.items:
            return None
        return self.items.pop(0)

# Funcion: peek
    def peek(self) -> Optional[Any]:
        # Devuelve el primer elemento sin sacarlo
        if not self.items:
            return None
        return self.items[0]

# Funcion: is_empty
    def is_empty(self):
        return len(self.items) == 0

# Funcion: to_list
    def to_list(self):
        # Copia de la cola como lista normal
        return list(self.items)


# ======================================================================
#region PILA (LIFO)
# ======================================================================
# Pila simple para registrar historial de acciones. Usamos LIFO para que
# la ultima accion quede al tope y sea facil de deshacer o revisar.
# ======================================================================

class Stack:
# Funcion: __init__
    def __init__(self):
        self.items: List[Any] = []

# Funcion: push
    def push(self, item):
        # Empila una accion o registro
        self.items.append(item)

# Funcion: pop
    def pop(self) -> Optional[Any]:
        # Desapila y devuelve el ultimo elemento
        if not self.items:
            return None
        return self.items.pop()

# Funcion: peek
    def peek(self):
        # Mira el ultimo elemento sin quitarlo
        if not self.items:
            return None
        return self.items[-1]

# Funcion: to_list
    def to_list(self):
        # Devuelve una copia de la pila como lista
        return list(self.items)


# ======================================================================
#region ARBOL GENERAL PARA CATEGORIAS
# ======================================================================
# Implementacion simple de un arbol general (n hijos). Cada TreeNode
# representa una categoria o subcategoria y contiene una lista de titulos.
# ======================================================================

@dataclass
class TreeNode:
    name: str
    books: List[str] = field(default_factory=list)
    children: List['TreeNode'] = field(default_factory=list)

# Funcion: add_child
    def add_child(self, child_name: str) -> 'TreeNode':
        # Si la subcategoria ya existe, la devuelve; si no, la crea
        for c in self.children:
            if c.name == child_name:
                return c
        new_child = TreeNode(child_name)
        self.children.append(new_child)
        return new_child

# Funcion: find
    def find(self, category_path: List[str]) -> Optional['TreeNode']:
        # Busca un nodo siguiendo el path, por ejemplo:
        # ["Biblioteca","Literatura","Novela"]
        # Si el primer elemento del path no coincide con este nodo, devuelve None
        if self.name != category_path[0]:
            return None

        # Si llegamos al ultimo segmento del path, este es el nodo buscado
        if len(category_path) == 1:
            return self

        # Sino, recursivamente buscar en los hijos
        for child in self.children:
            res = child.find(category_path[1:])
            if res:
                return res
        return None

# Funcion: add_book
    def add_book(self, category_path: List[str], book_title: str) -> bool:
        # Agrega un libro a la categoria indicada; si faltan subcategorias
        # las crea con add_child, luego agrega el titulo en la lista 'books'
        node = self
        if node.name != category_path[0]:
            # El path no es valido para esta raiz
            return False

        for part in category_path[1:]:
            node = node.add_child(part)

        node.books.append(book_title)
        return True

# Funcion: remove_book
    def remove_book(self, book_title: str):
        # Elimina el libro de esta categoría y de todas las subcategorías recursivamente
        if book_title in self.books:
            self.books.remove(book_title)
        for child in self.children:
            child.remove_book(book_title)

# Funcion: show
    def show(self, level=0, is_last=True, prefix=""):
        # Diseño visual tipo árbol con ramas y colores ANSI si consola lo soporta
        branch = "└── " if is_last else "├── "
        # ANSI color codes (azul para categorías, verde para libros)
        RESET = "\033[0m"
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        # Mostrar nombre de la categoría
        print(f"{prefix}{branch}{BLUE}{self.name}{RESET} ({len(self.books)} libros)")
        # Mostrar libros de la categoría
        for i, b in enumerate(self.books):
            is_last_book = (i == len(self.books) - 1) and not self.children
            book_branch = "    " if is_last else "│   "
            book_prefix = prefix + (book_branch if len(self.children) > 0 or not is_last_book else "    ")
            book_symbol = "└── " if is_last_book else "├── "
            print(f"{book_prefix}{book_symbol}{GREEN}{b}{RESET}")
        # Mostrar hijos (subcategorías)
        for idx, child in enumerate(self.children):
            is_last_child = idx == len(self.children) - 1
            child_prefix = prefix + ("    " if is_last else "│   ")
            child.show(level + 1, is_last_child, child_prefix)


# ======================================================================
#region GRAFO
# ======================================================================
# Grafo no dirigido usando lista de adyacencia (diccionario).
# Cada clave es un titulo y su valor es lista de titulos relacionados.
# ======================================================================

class Graph:
# Funcion: __init__
    def __init__(self):
        # adj almacena las listas de adyacencia: titulo -> [titulos relacionados]
        self.adj: Dict[str, List[str]] = {}

# Funcion: add_node
    def add_node(self, title: str):
        # Si el nodo no existe, crearlo con lista vacia
        if title not in self.adj:
            self.adj[title] = []

# Funcion: add_edge
    def add_edge(self, a: str, b: str):
        # Crea una arista no dirigida entre a y b
        # Aseguramos que ambos nodos existan
        self.add_node(a)
        self.add_node(b)

        # Añadir la relacion en ambas listas si no esta repetida
        if b not in self.adj[a]:
            self.adj[a].append(b)
        if a not in self.adj[b]:
            self.adj[b].append(a)

# Funcion: neighbors
    def neighbors(self, title: str) -> List[str]:
        # Devuelve la lista de vecinos (libros relacionados)
        return list(self.adj.get(title, []))

# Funcion: show
    def show(self):
        # Muestra el grafo: para cada libro imprime su lista de relacionados
        for k, vs in self.adj.items():
            print(f"{k}: {vs}")

# Funcion: related_by_two_steps
    def related_by_two_steps(self, title: str) -> List[str]:
        # Ejemplo de operacion en grafo: encontrar libros a distancia 2
        # Esto sirve para sugerir "amigos de amigos" (libros relacionados por via intermedia)
        res = set()
        direct = set(self.neighbors(title))
        for nb in direct:
            for nb2 in self.neighbors(nb):
                if nb2 != title and nb2 not in direct:
                    res.add(nb2)
        return list(res)


# ======================================================================
#region ALGORITMOS: BURBUJA, BUSQUEDAS
# ======================================================================
# Implementaciones basicas y explicadas de los algoritmos solicitados.
# Burbuja: sencillo de implementar, suficiente para volumenes pequenos.
# Busqueda secuencial: para listas no ordenadas.
# Busqueda binaria: para listas ya ordenadas (mejor rendimiento).
# ======================================================================

# Funcion: bubble_sort
def bubble_sort(items: List[Any], key=lambda x: x) -> List[Any]:
    # Ordena una copia de 'items' usando el criterio 'key'
    # Devuelve la lista ordenada (no modifica la original)
    arr = items[:]
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            # Si en una pasada no se intercambió nada, ya esta ordenado
            break
    return arr


# Funcion: sequential_search
def sequential_search(items: List[Any], predicate):
    # Recorre 'items' y devuelve el primer elemento que cumpla predicate
    for item in items:
        if predicate(item):
            return item
    return None


# Funcion: binary_search
def binary_search(sorted_items: List[Any], target, key=lambda x: x):
    # Busqueda binaria en lista ya ordenada segun 'key'
    lo, hi = 0, len(sorted_items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        mid_val = key(sorted_items[mid])
        if mid_val == target:
            return sorted_items[mid]
        elif mid_val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# ======================================================================
#region MODELOS DE DATOS
# ======================================================================
# Definicion de clases simples para Book y User. Son dataclasses para
# mayor claridad y menos codigo repetido.
# ======================================================================

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    available: bool = True  # True si el libro esta disponible

# Funcion: __str__
    def __str__(self):
        # Representacion legible del libro para imprimir en consola
        status = "Disponible" if self.available else "Prestado"
        return f"{self.title} by {self.author} (ISBN:{self.isbn}) - {status}"


@dataclass
class User:
    user_id: str
    name: str

# Funcion: __str__
    def __str__(self):
        return f"{self.user_id} - {self.name}"


# ======================================================================
#region SISTEMA PRINCIPAL DE BIBLIOTECA
# ======================================================================
# Clase que orquesta todas las estructuras: lista de libros, usuarios,
# cola de prestamos, pila de historial, arbol de categorias y grafo.
# ======================================================================

class Biblioteca:
# Funcion: __init__
    def __init__(self):
        # Inicializacion de todas las estructuras usadas por el sistema
        self.books = LinkedList()        # Almacen principal de Book
        self.users = LinkedList()        # Almacen de User
        self.loan_queue = Queue()        # Cola para solicitudes de prestamo
        self.history = Stack()           # Pila para historial de acciones
        self.categories = TreeNode("Biblioteca")  # Raiz del arbol de categorias
        self.relations = Graph()         # Grafo de relaciones entre libros
        self.cargar_datos()              # Cargar datos al iniciar

# Funcion: guardar_datos
    def guardar_datos(self, archivo="biblioteca_data.pkl"):
        # Guarda libros, usuarios, historial, categorías y relaciones en un archivo usando pickle
        datos = {
            "libros": self.books.to_list(),
            "usuarios": self.users.to_list(),
            "historial": self.history.to_list(),
            "categorias": self.categories,
            "relaciones": self.relations,
        }
        with open(archivo, "wb") as f:
            pickle.dump(datos, f)

# Funcion: cargar_datos
    def cargar_datos(self, archivo="biblioteca_data.pkl"):
        # Carga libros, usuarios, historial, categorías y relaciones desde un archivo pickle
        if not os.path.exists(archivo):
            return
        with open(archivo, "rb") as f:
            datos = pickle.load(f)
        # Restaurar libros
        self.books = LinkedList()
        for b in datos.get("libros", []):
            self.books.append(b)
        # Restaurar usuarios
        self.users = LinkedList()
        for u in datos.get("usuarios", []):
            self.users.append(u)
        # Restaurar historial
        self.history = Stack()
        for h in datos.get("historial", []):
            self.history.push(h)
        # Restaurar categorías (arbol)
        if "categorias" in datos and isinstance(datos["categorias"], TreeNode):
            self.categories = datos["categorias"]
        # Restaurar relaciones (grafo)
        if "relaciones" in datos and isinstance(datos["relaciones"], Graph):
            self.relations = datos["relaciones"]

    # ---------------- LIBROS ----------------
# Funcion: add_book
    def add_book(self, title: str, author: str, isbn: str):
        # Crea y agrega un Book a la lista ligada, y registra nodo en grafo
        book = Book(title, author, isbn)
        self.books.append(book)
        # Asegurar que el grafo tenga el nodo (aunque sin aristas aun)
        self.relations.add_node(title)
        # Registrar accion en historial
        self.history.push(f"|  Libro agregado: {title}")
        return book

# Funcion: find_book_by_isbn
    def find_book_by_isbn(self, isbn: str) -> Optional[Book]:
        # Busca por ISBN recorriendo la lista ligada
        return self.books.find(lambda b: b.isbn == isbn)

# Funcion: find_book_by_title
    def find_book_by_title(self, title: str) -> Optional[Book]:
        # Busca por titulo recorriendo la lista ligada
        return self.books.find(lambda b: b.title == title)

# Funcion: list_books
    def list_books(self):
        # Devuelve todos los libros como lista para iterar o mostrar
        return self.books.to_list()

# Funcion: sort_books_by_title
    def sort_books_by_title(self):
        # Ordena libros por titulo usando burbuja
        arr = self.list_books()
        sorted_arr = bubble_sort(arr, key=lambda b: b.title.lower())
        # Reconstruir la linked list con el orden nuevo
        self.books = LinkedList()
        for b in sorted_arr:
            self.books.append(b)
        self.history.push("|  Libros ordenados por titulo")

    # ---------------- USUARIOS ----------------
# Funcion: add_user
    def add_user(self, user_id: str, name: str):
        # Crea y agrega un usuario a la lista ligada
        user = User(user_id, name)
        self.users.append(user)
        self.history.push(f"|  Usuario agregado: {name}")
        return user

# Funcion: find_user
    def find_user(self, user_id: str) -> Optional[User]:
        # Busca un usuario por su id en la lista ligada
        return self.users.find(lambda u: u.user_id == user_id)

    # ---------------- PRESTAMOS ----------------
# Funcion: request_loan
    def request_loan(self, user_id: str, isbn: str):
        # Registra la solicitud de prestamo en la cola.
        # Validamos existencia de libro y usuario antes de encolar.
        book = self.find_book_by_isbn(isbn)
        user = self.find_user(user_id)

        if not book:
            return f"|  No existe libro con ISBN {isbn}"
        if not user:
            return f"|  No existe usuario con ID {user_id}"

        # Encolar la solicitud; se procesara por orden FIFO
        self.loan_queue.enqueue((user_id, isbn))
        self.history.push(f"|  Solicitud prestamo: {user_id} -> {isbn}")
        return "|  Solicitud registrada"

# Funcion: process_next_loan
    def process_next_loan(self):
        # Procesa la siguiente solicitud en la cola
        req = self.loan_queue.dequeue()
        if not req:
            return "|  No hay solicitudes"

        user_id, isbn = req
        book = self.find_book_by_isbn(isbn)

        if book and book.available:
            # Asignar el libro al usuario (marcar como no disponible)
            book.available = False
            self.history.push(f"|  Prestamo procesado: {user_id} obtuvo {isbn}")
            return f"|  Prestamo concedido -> {user_id} obtiene {book.title}"

        # Si no esta disponible o libro no existe, fallo
        self.history.push(f"|  Prestamo fallido: {user_id} -> {isbn}")
        return "|  El libro no esta disponible"

# Funcion: return_book
    def return_book(self, isbn: str):
        # Marca el libro como disponible al devolverlo
        book = self.find_book_by_isbn(isbn)
        if not book:
            return "|  Libro no encontrado"
        book.available = True
        self.history.push(f"|  Devolucion: {isbn}")
        return f"|  Libro {book.title} devuelto"

    # ---------------- CATEGORIAS ----------------
# Funcion: add_category
    def add_category(self, path: List[str]):
        # Añade una categoria siguiendo un path como ["Biblioteca","Ciencia","Fisica"]
        # Requiere que el primer elemento sea el nombre de la raiz actual
        if not path or path[0] != self.categories.name:
            return False

        node = self.categories
        for part in path[1:]:
            node = node.add_child(part)

        self.history.push(f"|  Categoria agregada: {'/'.join(path)}")
        return True

# Funcion: add_book_to_category
    def add_book_to_category(self, category_path: List[str], isbn: str):
        # Agrega el titulo de un libro a una categoria del arbol
        book = self.find_book_by_isbn(isbn)
        if not book:
            return "|  Libro no encontrado"

        ok = self.categories.add_book(category_path, book.title)
        if ok:
            self.history.push(f"|  Libro {book.title} agregado a {'/'.join(category_path)}")
            return "|  Libro agregado"
        return "|  Categoria no existente"

    # ---------------- RELACIONES ENTRE LIBROS (GRAFO) ----------------
# Funcion: relate_books
    def relate_books(self, title_a: str, title_b: str):
        # Crea una relacion entre dos titulos en el grafo
        self.relations.add_edge(title_a, title_b)
        self.history.push(f"|  Relacion creada: {title_a} <-> {title_b}")
        return "|  Relacion registrada"

# Funcion: related_books
    def related_books(self, title: str) -> List[str]:
        # Devuelve la lista de libros relacionados a un titulo
        return self.relations.neighbors(title)

    # ---------------- REPORTES ----------------
# Funcion: show_history
    def show_history(self, n=10):
        # Muestra las ultimas n acciones registradas en la pila (top es ultima)
        for h in reversed(self.history.to_list()[-n:]):
            print(h)

# Funcion: show_categories
    def show_categories(self):
        # Muestra el arbol de categorias desde la raiz
        self.categories.show()

# Funcion: show_relations
    def show_relations(self):
        # Muestra el grafo de relaciones (lista de adyacencia)
        self.relations.show()

# Funcion: mostrar_tabla_en_ventana
def mostrar_tabla_en_ventana(tabla_str, titulo="Tabla"):
    ventana = tk.Tk()
    ventana.title(titulo)
    text_area = scrolledtext.ScrolledText(ventana, width=100, height=20, font=("Consolas", 10))
    text_area.pack(fill=tk.BOTH, expand=True)
    text_area.insert(tk.END, tabla_str)
    text_area.config(state=tk.DISABLED)
    ventana.mainloop()

# ======================================================================
#region MENU INTERACTIVO
# ======================================================================
# Menu por consola para que un usuario pueda usar el sistema sin tocar
# el codigo. Cada opcion realiza una accion sobre las estructuras
# y le mantengo mensajes simples y claras instrucciones sobre formato
# ======================================================================

# Funcion: limpiar_pantalla
def limpiar_pantalla():
    # Limpia la pantalla de la consola (Windows y Unix)
    os.system('cls' if os.name == 'nt' else 'clear')

# Funcion: menu_libros
def menu_libros(lib):
    while True:
        limpiar_pantalla()
        print("|--------------------------|         LIBROS         |--------------------------|")
        print("| 1. Agregar libro           2. Eliminar libro         3. Mostrar libros       |")
        print("| 4. Buscar por titulo       5. Buscar por ISBN        6. Ordenar por titulo   |")
        print("|                         0. Volver al menú principal                          |")
        print("|------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción: ")
        match op:
            case "1":
                title = input("|  Titulo: ")
                author = input("|  Autor: ")
                isbn = input("|  ISBN: ")
                # Validar campos vacíos
                if not title.strip() or not author.strip() or not isbn.strip():
                    print("|  Ningún campo puede estar vacío.")
                    input("|  Presione Enter para continuar...")
                    continue
                # Evitar duplicados de ISBN
                if lib.find_book_by_isbn(isbn):
                    print("|  Ya existe un libro con ese ISBN. Intente con otro.")
                    input("|  Presione Enter para continuar...")
                    continue
                lib.add_book(title, author, isbn)
                print("|  Libro agregado correctamente.")
                input("|  Presione Enter para continuar...")
            case "2":
                isbn = input("|  ISBN del libro a eliminar: ")
                libro_a_eliminar = lib.find_book_by_isbn(isbn)
                eliminado = lib.books.remove(lambda b: b.isbn == isbn)
                if eliminado:
                    # Eliminar el nodo del grafo y sus relaciones si el libro es eliminado
                    if libro_a_eliminar:
                        lib.relations.adj.pop(libro_a_eliminar.title, None)
                        for vecinos in lib.relations.adj.values():
                            if libro_a_eliminar.title in vecinos:
                                vecinos.remove(libro_a_eliminar.title)
                    # Eliminar de la cola de préstamos cualquier solicitud pendiente de este libro
                    nueva_cola = Queue()
                    while not lib.loan_queue.is_empty():
                        req = lib.loan_queue.dequeue()
                        if req[1] != isbn:
                            nueva_cola.enqueue(req)
                    lib.loan_queue = nueva_cola
                    # Eliminar de todas las categorías del árbol
                    if libro_a_eliminar:
                        lib.categories.remove_book(libro_a_eliminar.title)
                print("|  Libro eliminado." if eliminado else "|  No se encontró el libro.")
                input("|  Presione Enter para continuar...")
            case "3":
                libros = lib.list_books()
                if libros:
                    tabla = [
                        [str(b.title), str(b.author), str(b.isbn), "Disponible" if b.available else "Prestado"]
                        for b in libros
                    ]
                    print(tabulate(tabla, headers=["Titulo", "Autor", "ISBN", "Estado"], tablefmt="grid", stralign="center"))
                else:
                    print("|  No hay libros registrados.")
                input("|  Presione Enter para continuar...")
            case "4":
                title = input("|  Titulo: ")
                res = lib.find_book_by_title(title)
                if res:
                    tabla = [
                        [str(res.title), str(res.author), str(res.isbn), "Disponible" if res.available else "Prestado"]
                    ]
                    print(tabulate(tabla, headers=["Titulo", "Autor", "ISBN", "Estado"], tablefmt="grid", stralign="center"))
                else:
                    print("|  No encontrado.")
                input("|  Presione Enter para continuar...")
            case "5":
                isbn = input("|  ISBN: ")
                res = lib.find_book_by_isbn(isbn)
                if res:
                    tabla = [
                        [str(res.title), str(res.author), str(res.isbn), "Disponible" if res.available else "Prestado"]
                    ]
                    print(tabulate(tabla, headers=["Titulo", "Autor", "ISBN", "Estado"], tablefmt="grid", stralign="center"))
                else:
                    print("|  No encontrado.")
                input("|  Presione Enter para continuar...")
            case "6":
                lib.sort_books_by_title()
                print("|  Libros ordenados.")
                input("|  Presione Enter para continuar...")
            case "0":
                break
            case _:
                print("|  Opción inválida.")
                input("|  Presione Enter para continuar...")

# Funcion: menu_usuarios
def menu_usuarios(lib):
    while True:
        limpiar_pantalla()
        print("|--------------------------|        USUARIOS        |--------------------------|")
        print("| 1. Agregar usuario         2. Eliminar usuario        3. Mostrar usuarios    |")
        print("|                        0. Volver al menú principal                           |")
        print("|------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción: ")
        match op:
            case "1":
                uid = input("|  ID de usuario: ")
                # Evitar duplicados de ID de usuario
                if not uid.strip():
                    print("|  El ID no puede estar vacío.")
                    input("|  Presione Enter para continuar...")
                    continue
                if lib.find_user(uid):
                    print("|  Ya existe un usuario con ese ID. Intente con otro.")
                    input("|  Presione Enter para continuar...")
                    continue
                name = input("|  Nombre: ")
                if not name.strip():
                    print("|  El nombre no puede estar vacío.")
                    input("|  Presione Enter para continuar...")
                    continue
                lib.add_user(uid, name)
                print("|  Usuario registrado.")
                input("|  Presione Enter para continuar...")
            case "2":
                uid = input("|  ID de usuario a eliminar: ")
                eliminado = lib.users.remove(lambda u: u.user_id == uid)
                # Eliminar préstamos pendientes de la cola si el usuario es eliminado
                if eliminado:
                    nueva_cola = Queue()
                    while not lib.loan_queue.is_empty():
                        req = lib.loan_queue.dequeue()
                        if req[0] != uid:
                            nueva_cola.enqueue(req)
                    lib.loan_queue = nueva_cola
                print("|  Usuario eliminado." if eliminado else "|  No se encontró el usuario.")
                input("|  Presione Enter para continuar...")
            case "3":
                usuarios = lib.users.to_list()
                if usuarios:
                    tabla = [
                        [str(u.user_id), str(u.name)]
                        for u in usuarios
                    ]
                    print(tabulate(tabla, headers=["ID", "Nombre"], tablefmt="grid", stralign="center"))
                else:
                    print("|  No hay usuarios registrados.")
                input("|  Presione Enter para continuar...")
            case "0":
                break
            case _:
                print("|  Opción inválida.")
                input("|  Presione Enter para continuar...")

# Funcion: menu_prestamos
def menu_prestamos(lib):
    while True:
        limpiar_pantalla()
        print("|--------------------------|        PRESTAMOS        |--------------------------|")
        print("| 1. Solicitar prestamo      2. Procesar prestamo      3. Devolver libro        |")
        print("|                        0. Volver al menú principal                            |")
        print("|-------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción: ")
        match op:
            case "1":
                uid = input("|  ID usuario: ")
                # Mostrar mensaje si el usuario no existe antes de pedir ISBN
                if not lib.find_user(uid):
                    print("|  No existe usuario con ese ID.")
                    input("|  Presione Enter para continuar...")
                    continue
                isbn = input("|  ISBN libro: ")
                # Validar que el libro exista
                if not lib.find_book_by_isbn(isbn):
                    print("|  No existe libro con ese ISBN.")
                    input("|  Presione Enter para continuar...")
                    continue
                # Evitar que el usuario solicite el mismo libro varias veces
                if any(req[0] == uid and req[1] == isbn for req in lib.loan_queue.to_list()):
                    print("|  Ya existe una solicitud pendiente para este libro y usuario.")
                    input("|  Presione Enter para continuar...")
                    continue
                print(lib.request_loan(uid, isbn))
                input("|  Presione Enter para continuar...")
            case "2":
                print(lib.process_next_loan())
                input("|  Presione Enter para continuar...")
            case "3":
                isbn = input("|  ISBN a devolver: ")
                print(lib.return_book(isbn))
                input("|  Presione Enter para continuar...")
            case "0":
                break
            case _:
                print("|  Opción inválida.")
                input("|  Presione Enter para continuar...")

# Funcion: menu_categorias
def menu_categorias(lib):
    while True:
        limpiar_pantalla()
        print("|--------------------------|       CATEGORIAS        |--------------------------|")
        print("| 1. Agregar categoria       2. Eliminar categoria      3. Mostrar categorias   |")
        print("| 4. Agregar libro a categoria                      0. Volver al menú principal |")
        print("|-------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción: ")
        match op:
            case "1":
                print("|  Formato: Biblioteca/Categoria/Subcategoria")
                path_str = input("|  Ruta: ")
                path = path_str.split("/")
                if lib.add_category(path):
                    print("|  Categoria creada.")
                else:
                    print("|  Ruta invalida. El primer elemento debe ser 'Biblioteca'.")
                input("|  Presione Enter para continuar...")
            case "2":
                print("|  Formato: Biblioteca/Categoria/Subcategoria")
                path_str = input("|  Ruta: ")
                path = path_str.split("/")
                if len(path) < 2:
                    print("|  Ruta inválida.")
                else:
                    padre = lib.categories.find(path[:-1])
                    if padre:
                        hijo = [c for c in padre.children if c.name == path[-1]]
                        if hijo:
                            padre.children.remove(hijo[0])
                            print("|  Categoría eliminada.")
                        else:
                            print("|  No se encontró la subcategoría.")
                    else:
                        print("|  No se encontró la ruta padre.")
                input("|  Presione Enter para continuar...")
            case "3":
                lib.show_categories()
                input("|  Presione Enter para continuar...")
            case "4":
                print("|  Formato: Biblioteca/Categoria/Subcategoria")
                path_str = input("|  Ruta: ")
                isbn = input("|  ISBN libro: ")
                path = path_str.split("/")
                print(lib.add_book_to_category(path, isbn))
                input("|  Presione Enter para continuar...")
            case "0":
                break
            case _:
                print("|  Opción inválida.")
                input("|  Presione Enter para continuar...")

# Funcion: menu_relaciones
def menu_relaciones(lib):
    from tkinter import Canvas, Toplevel
    import math

# Funcion: mostrar_grafo_en_ventana
    def mostrar_grafo_en_ventana(grafo, titulo="Relaciones entre libros (Grafo)"):
        nodos = list(grafo.adj.keys())
        n = len(nodos)
        if n == 0:
            print("|  No hay relaciones registradas.")
            return
        ventana = Toplevel()
        ventana.title(titulo)
        ancho = 700
        alto = 500
        canvas = Canvas(ventana, width=ancho, height=alto, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)
        radio = min(ancho, alto) // 2 - 60
        centro_x, centro_y = ancho // 2, alto // 2
        pos = {}
        for i, nodo in enumerate(nodos):
            ang = 2 * math.pi * i / n
            x = centro_x + radio * math.cos(ang)
            y = centro_y + radio * math.sin(ang)
            pos[nodo] = (x, y)
        for nodo, vecinos in grafo.adj.items():
            x1, y1 = pos[nodo]
            for vecino in vecinos:
                if vecino in pos:
                    x2, y2 = pos[vecino]
                    if nodos.index(nodo) < nodos.index(vecino):
                        canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
        r_nodo = 25
        for nodo, (x, y) in pos.items():
            canvas.create_oval(x - r_nodo, y - r_nodo, x + r_nodo, y + r_nodo, fill="#cce5ff", outline="#333", width=2)
            canvas.create_text(x, y, text=nodo, font=("Arial", 10, "bold"), width=80)
        ventana.mainloop()

    while True:
        limpiar_pantalla()
        print("|--------------------------| RELACIONES ENTRE LIBROS (GRAFO) |--------------------------|")
        print("| 1. Relacionar libros        2. Eliminar relación        3. Ver relaciones (grafo)     |")
        print("|                           0. Volver al menú principal                                 |")
        print("|---------------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción: ")
        match op:
            case "1":
                print("|  Relacionar libros permite vincular dos libros para indicar que")
                print("|  están conectados (por temática, autor, saga, etc).")
                a = input("|  Titulo A (primer libro): ")
                b = input("|  Titulo B (segundo libro): ")
                # Cambié aquí: ahora comprueba existencia de ambos libros antes de relacionar
                libro_a = lib.find_book_by_title(a)
                libro_b = lib.find_book_by_title(b)
                if not libro_a or not libro_b:
                    print("|  Ambos libros deben existir para crear la relación.")
                elif a == b:
                    print("|  No se puede relacionar un libro consigo mismo.")
                else:
                    print(lib.relate_books(a, b))
                input("|  Presione Enter para continuar...")

            case "2":
                a = input("|  Titulo A: ")
                b = input("|  Titulo B: ")
                # Validar existencia de ambos titulos en el grafo
                if a in lib.relations.adj and b in lib.relations.adj[a]:
                    lib.relations.adj[a].remove(b)
                if b in lib.relations.adj and a in lib.relations.adj[b]:
                    lib.relations.adj[b].remove(a)
                print("|  Relación eliminada")
                input("|  Presione Enter para continuar...")

            case "3":
                mostrar_grafo_en_ventana(lib.relations)
                input("|  Presione Enter para continuar...")

            case "0":
                break
            
            case _:
                print("|  Opción inválida.")
                input("|  Presione Enter para continuar...")

# Funcion: menu_historial
def menu_historial(lib):
    limpiar_pantalla()
    print("|--------------------------|         HISTORIAL        |--------------------------|")
    lib.show_history(20)
    input("|  Presione Enter para continuar...")

# Funcion: menu
def menu():
    lib = Biblioteca()
    while True:
        limpiar_pantalla()
        print("|------------------------------------------------------------------------------------------|")
        print("|                          |        BIBLIOTECA INTELIGENTE      |                          |")
        print("|------------------------------------------------------------------------------------------|")
        print("|                          |  1. Libros                         |                          |")
        print("|                          |  2. Usuarios                       |                          |")
        print("|                          |  3. Préstamos                      |                          |")
        print("|                          |  4. Categorías                     |                          |")
        print("|                          |  5. Relaciones entre libros        |                          |")
        print("|                          |  6. Historial                      |                          |")
        print("|                          |  0. Guardar y Salir                |                          |")
        print("|------------------------------------------------------------------------------------------|")
        op = input("|  Seleccione una opción -> ")
        match op:
            case "1":
                menu_libros(lib)
            case "2":
                menu_usuarios(lib)
            case "3":
                menu_prestamos(lib)
            case "4":
                menu_categorias(lib)
            case "5":
                menu_relaciones(lib)
            case "6":
                menu_historial(lib)
            case "0":
                limpiar_pantalla()
                print("|  SALIENDO DEL SISTEMA")
                lib.guardar_datos()
                break
            case _:
                limpiar_pantalla()

# ======================================================================
#region EJECUTAR MENU POR DEFECTO
# ======================================================================

if __name__ == "__main__":
    menu()