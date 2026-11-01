# =====================================================================
#  lista_python.py  —  LISTA 2: con el list de PYTHON (built-in)
# ---------------------------------------------------------------------
#  Mismas operaciones que la Lista 1, pero ahora usamos lo que Python
#  ya trae: append, insert, pop, remove, sort, reverse, copy, len,
#  enumerate, bisect ... y LIST COMPREHENSIONS.
#
#      self.pasajeros -> [Pasajero, Pasajero, ...]   (crece sola)
#
#  ✅ COMPRENSIONES de listas en:
#       buscar · buscar_binaria · eliminar_por_valor (versión 2)
#       filtrar_mayores_de_edad · nombres_en_mayusculas
#
#  Sintaxis:
#       [EXPRESIÓN for ELEMENTO in LISTA]            -> transformar
#       [ELEMENTO  for ELEMENTO in LISTA if COND]    -> filtrar
# =====================================================================

from bisect import bisect_left
from pasajero import Pasajero


class ListaPasajerosPython:

    def __init__(self):
        self.pasajeros = []               # list de Python: crece sola

    # -----------------------------------------------------------------
    # AÑADIR  (con la mejora: no permite cédulas repetidas)
    # -----------------------------------------------------------------
    def añadir(self, pasajero):
        """Añade al final con append(), si la cédula no existe."""
        if self.buscar(pasajero.cedula) != -1:
            print("⚠ Ya existe un pasajero con esa cédula")
            return False
        self.pasajeros.append(pasajero)
        return True

    # -----------------------------------------------------------------
    # LISTAR
    # -----------------------------------------------------------------
    def listar(self):
        """Muestra los pasajeros con su posición usando enumerate()."""
        if not self.pasajeros:                  # lista vacía es False
            print("(lista vacía)")
            return
        for i, p in enumerate(self.pasajeros):
            print(f"[{i}] {p}")

    # -----------------------------------------------------------------
    # LONGITUD
    # -----------------------------------------------------------------
    def longitud(self):
        """Retorna cuántos pasajeros hay."""
        return len(self.pasajeros)

    # -----------------------------------------------------------------
    # INSERTAR
    # -----------------------------------------------------------------
    def insertar(self, posicion, pasajero):
        """Mete el pasajero en 'posicion' con insert()."""
        if posicion < 0 or posicion > len(self.pasajeros):
            print("⚠ Posición no válida")
            return False
        if self.buscar(pasajero.cedula) != -1:
            print("⚠ Ya existe un pasajero con esa cédula")
            return False
        self.pasajeros.insert(posicion, pasajero)
        # RESPUESTA (¿Python corre los elementos?): SÍ. insert() desplaza
        # a la derecha todos los elementos desde 'posicion'. No lo vemos,
        # pero el trabajo sigue ahí: es O(n) (crece con la cantidad de
        # elementos). append() al final, en cambio, es O(1) amortizado.
        return True

    # -----------------------------------------------------------------
    # BUSCAR POR CÉDULA  (con COMPRENSIÓN)
    # -----------------------------------------------------------------
    def buscar(self, cedula):
        """Retorna la posición (int) o -1."""
        posiciones = [i for i, p in enumerate(self.pasajeros)
                      if p.cedula == cedula]
        if not posiciones:
            return -1
        return posiciones[0]
        # EXTRA con next():
        # return next((i for i, p in enumerate(self.pasajeros)
        #              if p.cedula == cedula), -1)

    # -----------------------------------------------------------------
    # BUSCAR BINARIA  (con COMPRENSIÓN + bisect)
    # -----------------------------------------------------------------
    def buscar_binaria(self, cedula):
        """REQUISITO: lista ordenada por cédula (ordenar_asc antes)."""
        cedulas = [p.cedula for p in self.pasajeros]     # COMPRENSIÓN
        i = bisect_left(cedulas, cedula)    # dónde "debería" estar
        if i < len(cedulas) and cedulas[i] == cedula:
            return i
        return -1

    # -----------------------------------------------------------------
    # MODIFICAR
    # -----------------------------------------------------------------
    def modificar(self, cedula, nuevo_nombre, nueva_edad):
        """Cambia nombre y edad del pasajero con esa cédula."""
        pos = self.buscar(cedula)
        if pos == -1:
            print("⚠ No existe un pasajero con esa cédula")
            return False
        self.pasajeros[pos].nombre = nuevo_nombre
        self.pasajeros[pos].edad = nueva_edad
        return True

    # -----------------------------------------------------------------
    # ELIMINAR POR POSICIÓN
    # -----------------------------------------------------------------
    def eliminar_por_posicion(self, posicion):
        """Quita con pop() y retorna el eliminado (o None)."""
        if posicion < 0 or posicion >= len(self.pasajeros):
            print("⚠ Posición no válida")
            return None
        return self.pasajeros.pop(posicion)

    # -----------------------------------------------------------------
    # ELIMINAR POR VALOR (por cédula)  — dos formas
    # -----------------------------------------------------------------
    def eliminar_por_valor(self, cedula):
        """Quita el pasajero que tenga esa cédula."""
        # FORMA 1 (remove) — comentada para comparar:
        # pos = self.buscar(cedula)
        # if pos == -1:
        #     print("⚠ No existe un pasajero con esa cédula")
        #     return False
        # self.pasajeros.remove(self.pasajeros[pos])
        # return True

        # FORMA 2 (COMPRENSIÓN) — la que queda activa:
        antes = len(self.pasajeros)
        self.pasajeros = [p for p in self.pasajeros if p.cedula != cedula]
        if len(self.pasajeros) < antes:       # True si eliminó algo
            return True
        print("⚠ No existe un pasajero con esa cédula")
        return False

    # -----------------------------------------------------------------
    # ORDENAR ASCENDENTE (por cédula)
    # -----------------------------------------------------------------
    def ordenar_asc(self):
        """Ordena de menor a mayor cédula."""
        self.pasajeros.sort(key=lambda p: p.cedula)
        # RESPUESTA: key= es una función que sort() aplica a CADA elemento
        # para obtener el valor por el que va a comparar (aquí, la cédula).
        # Sin key=, sort() intentaría comparar objetos Pasajero entre sí y
        # falla con: TypeError: '<' not supported between instances of
        # 'Pasajero' and 'Pasajero'.

    # -----------------------------------------------------------------
    # ORDENAR DESCENDENTE (por cédula)
    # -----------------------------------------------------------------
    def ordenar_desc(self):
        """Ordena de MAYOR a menor cédula."""
        self.pasajeros.sort(key=lambda p: p.cedula, reverse=True)

    # -----------------------------------------------------------------
    # REVERSAR
    # -----------------------------------------------------------------
    def reversar(self):
        """Invierte el orden (no es lo mismo que ordenar_desc)."""
        self.pasajeros.reverse()

    # -----------------------------------------------------------------
    # COPIAR
    # -----------------------------------------------------------------
    def copiar(self):
        """Retorna otra ListaPasajerosPython con los mismos pasajeros."""
        nueva = ListaPasajerosPython()
        nueva.pasajeros = self.pasajeros.copy()    # o self.pasajeros[:]
        return nueva
        # RESPUESTA: es una copia SUPERFICIAL. Las dos LISTAS son distintas
        # (reversar la copia no cambia el original), pero los objetos
        # Pasajero de adentro son los MISMOS. Por eso, si modificas a un
        # pasajero de la copia, el cambio también se ve en el original:
        # las dos listas apuntan al mismo objeto en memoria.

    # -----------------------------------------------------------------
    # FILTRAR MAYORES DE EDAD  (COMPRENSIÓN que FILTRA)
    # -----------------------------------------------------------------
    def filtrar_mayores_de_edad(self):
        """Retorna una NUEVA lista solo con los de 18 años o más."""
        nueva = ListaPasajerosPython()
        nueva.pasajeros = [p for p in self.pasajeros if p.es_mayor_de_edad()]
        return nueva

    # -----------------------------------------------------------------
    # NOMBRES EN MAYÚSCULAS  (COMPRENSIÓN que TRANSFORMA)
    # -----------------------------------------------------------------
    def nombres_en_mayusculas(self):
        """Retorna una list de str con los nombres en mayúsculas."""
        return [p.nombre.upper() for p in self.pasajeros]