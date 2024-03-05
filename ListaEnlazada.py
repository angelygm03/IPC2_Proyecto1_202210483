from NodoDato import NodoDato
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = NodoDato(dato)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo

    def buscar(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.dato.nombre == nombre_piso:
                return actual.dato
            actual = actual.siguiente
        return None