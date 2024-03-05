from ListaEnlazada import ListaEnlazada

class NodoInstruccion:
    def __init__(self, instruccion=None, siguiente=None):
        self.instruccion = instruccion
        self.siguiente = siguiente

def calcular_costo_minimo(patron_origen, patron_destino, F, S):
    costo = 0
    instrucciones = None

    cambios = 0
    cambios_maximos = 2

    instrucciones = ListaEnlazada()

    for i in range(len(patron_origen)):
        if patron_origen[i] != patron_destino[i]:
            cambios += 1

            if cambios <= cambios_maximos:
                if costo + F <= S:
                    costo += F
                    instrucciones.agregar(f"Voltear el azulejo en la posición {i + 1}")
                else:
                    costo += S
                    instrucciones.agregar(f"Intercambiar el azulejo en la posición {i + 1} con el siguiente")
            else:
                costo += S
                instrucciones.agregar(f"Intercambiar el azulejo en la posición {i + 1} con el siguiente")

    if cambios > 0 and instrucciones is not None:
        return costo, instrucciones
    else:
        return None, None
