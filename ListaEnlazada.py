from NodoDato import NodoDato
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo_nodo = NodoDato(dato)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def buscar_piso(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.dato.nombre == nombre_piso:
                return actual 
            actual = actual.siguiente
        return None