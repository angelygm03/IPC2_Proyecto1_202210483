from NodoPiso import NodoPiso

class ListaPisos:
    def __init__(self):
        self.cabeza = None

    def agregar_piso(self, nombre, R, C, F, S, patrones):
        nuevo_piso = NodoPiso(nombre, R, C, F, S, patrones)
        if not self.cabeza:
            self.cabeza = nuevo_piso
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_piso

    def buscar_piso(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre_piso:
                return actual
            actual = actual.siguiente
        return None