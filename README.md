# 📘 Manual de Usuario del Sistema: Biblioteca Inteligente

---

## 1. Introducción al uso del sistema

Este manual explica cómo interactuar con el sistema **Biblioteca Inteligente**, una aplicación de consola intuitiva y estructurada por menús. Cada opción del menú representa una acción específica, desde el registro de libros y usuarios hasta el manejo de préstamos, categorías y relaciones entre libros.

El sistema está diseñado para que cualquier persona, con o sin experiencia en programación, pueda utilizarlo fácilmente. Basta con ingresar el número de la opción deseada y seguir las instrucciones en pantalla.

---

## 2. Acceso al sistema

Para iniciar el sistema, ejecuta el archivo principal del proyecto en Python. Al hacerlo, se mostrará el siguiente menú mas o menos asi:

                                          -----------------------------------------------------------
                                                              BIBLIOTECA INTELIGENTE                
                                          -----------------------------------------------------------
                                          1. Libros
                                          2. Usuarios
                                          3. Prestamos
                                          4. Categorias
                                          5. Relaciones entre libros
                                          6. Historial
                                          0. Guardar y salir
                                          -----------------------------------------------------------
                                          Ingrese una opcion:


ESO SI. Solo debes escribir el número de la opción deseada y presionar Enter.

---

## 3. Descripción general de las funciones

### 3.1 Módulo de Libros

Permite administrar la información de los libros registrados.

**Funciones disponibles:**
- **Agregar libro:** Solicita título, autor e ISBN. Se almacena en una lista ligada.
- **Buscar libro por ISBN:** Localiza un libro por su código único.
- **Listar libros:** Muestra todos los libros registrados.
- **Ordenar libros por título:** Ordena alfabéticamente usando el algoritmo de burbuja.

---

### 3.2 Módulo de Usuarios

Gestiona la información de los usuarios.

**Funciones disponibles:**
- **Registrar usuario:** Solicita ID único y nombre. Se almacena en una lista ligada.
- **Buscar usuario por ID:** Muestra la información si existe.
- **Listar usuarios:** Muestra todos los usuarios registrados.

---

### 3.3 Módulo de Préstamos

Simula el préstamo de libros usando una cola (FIFO).

**Funciones disponibles:**
- **Solicitar préstamo:** Ingresar ID de usuario e ISBN del libro.
- **Procesar siguiente préstamo:** Atiende la primera solicitud en orden.
- **Devolver libro:** Marca el libro como disponible.

---

### 3.4 Módulo de Categorías

Organiza los libros en un árbol de categorías.

**Funciones disponibles:**
- **Agregar categoría:** Ingresar ruta completa (ej. `Biblioteca/Literatura/Novela`).
- **Agregar libro a categoría:** Ruta + ISBN.
- **Mostrar categorías:** Imprime el árbol completo.

---

### 3.5 Módulo de Relaciones entre Libros

Usa un grafo no dirigido para conectar libros.

**Funciones disponibles:**
- **Relacionar libros:** Ingresar títulos de dos libros.
- **Mostrar relaciones:** Imprime cada libro y sus conexiones.

---

### 3.6 Módulo de Historial

Utiliza una pila (LIFO) para registrar acciones recientes.

**Función disponible:**
- **Mostrar historial:** Muestra las últimas acciones realizadas.

---

### 3.7 Guardar y salir

Guarda toda la información y finaliza el programa. Es importante usar esta opción para no perder datos.

---

## 4. Consejos de uso para evitar errores

- Verificar siempre el ISBN antes de ingresarlo.
- Registrar usuarios antes de solicitar préstamos.
- Usar rutas correctas para categorías (con `/`).
- Evitar duplicar títulos o IDs.
- Procesar préstamos antes de agregar nuevos.
- Guardar antes de salir.

---

## 5. Solución de problemas comunes

| Situación                 | Posible causa      | Qué hacer                  |
|--------------------------|--------------------|----------------------------|
| Libro no aparece          | ISBN incorrecto    | Revisar y reingresar datos |
| Usuario no aparece        | ID no existente    | Registrarlo nuevamente     |
| No se puede prestar libro | Libro ya prestado  | Esperar devolución         |
| Categoría no se encuentra | Ruta mal escrita   | Revisar el formato         |
| Relación no creada        | Título mal escrito | Revisar ortografía         |

Cabe recalcar tambien **este archivo trae consigo una librera "Tabulate"** las demas tendras que instalarlas si es necesario.

## 6. Cierre

El sistema **Biblioteca Inteligente** está pensado para ser práctico, sencillo y completo. Este manual cortito resume sus funciones esenciales y sirve como guía para cualquier usuario que desee interactuar con el programa sin dificultad.

