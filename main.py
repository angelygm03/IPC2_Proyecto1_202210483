import xml.etree.ElementTree as ET
from graphviz import Digraph
from NodoPiso import NodoPiso
from ListaEnlazada import ListaEnlazada
from NodoInstruccion import calcular_costo_minimo


def menu():
    print()
    print("Menú Principal")
    print("1. Mostrar gráficamente el patrón.")
    print("2. Seleccionar un nuevo código de patrón")
    print("3. Mostrar pisos cargados")
    print("4. Salir")

def mostrar_patron(patron_data, R, C):
    dot = Digraph(comment='Patrón')
    dot.node('tab', label=f'<<TABLE>{generate_table(patron_data, R, C)}</TABLE>>', shape='none')
    dot.render('patron', format='png', cleanup=True)
    print("El patrón se ha mostrado gráficamente.")

def seleccionar_codigo_patron(piso):
    codigo_patron = input("Ingrese el código del patrón deseado: ")
    patron_data = None
    actual = piso.patrones.cabeza
    while actual:
        codigo, patron = actual.dato
        if codigo == codigo_patron:
            patron_data = patron
            break
        actual = actual.siguiente

    if patron_data is None:
        print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
        return
    
    nuevo_codigo = input("Ingrese el nuevo código de patrón: ")
    costo, instrucciones = calcular_costo_minimo(patron, patron_data, piso.S, piso.F)

    if instrucciones is None:
        print("No se encontraron instrucciones para realizar el cambio.")
        return

    print(f"El costo mínimo para realizar el cambio hacia el nuevo patrón es: {costo} Quetzales.")
    opcion = input("¿Desea mostrar las instrucciones en consola o en un archivo? (consola/archivo): ").lower()
    if opcion == "consola":
        for instruccion in instrucciones:
            print(instruccion)
    elif opcion == "archivo":
        with open("instrucciones.txt", "w") as f:
            for instruccion in instrucciones:
                f.write(instruccion + "\n")
        print("Las instrucciones se han guardado en el archivo 'instrucciones.txt'.")
    else:
        print("Opción no válida.")


def mostrar_instrucciones(instrucciones):
    actual = instrucciones
    while actual:
        print(actual.instruccion)
        actual = actual.siguiente

def guardar_instrucciones_en_archivo(instrucciones):
    with open("instrucciones.txt", "w") as f:
        actual = instrucciones
        while actual:
            f.write(actual.instruccion + "\n")
            actual = actual.siguiente
    print("Las instrucciones se han guardado en el archivo 'instrucciones.txt'.")

def mostrar_pisos_y_patrones(lista_pisos):
    actual = lista_pisos.cabeza
    while actual:
        piso = actual.dato
        print(f"Piso: {piso.nombre}")
        print("Códigos de patrones disponibles:")
        actual_patron = piso.patrones.cabeza
        while actual_patron:
            codigo, _ = actual_patron.dato
            print(f"- Código: {codigo}")
            actual_patron = actual_patron.siguiente
        print()
        actual = actual.siguiente

def read_xml(filename):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        lista_pisos = ListaEnlazada()
        for piso in root.findall('piso'):
            nombre = piso.get('nombre')
            R = int(piso.find('R').text)
            C = int(piso.find('C').text)
            F = int(piso.find('F').text)
            S = int(piso.find('S').text)
            patrones = ListaEnlazada()
            for patron in piso.find('patrones').findall('patron'):
                codigo = patron.get('codigo')
                patron_data = patron.text.strip()
                patrones.agregar((codigo, patron_data))
            nuevo_piso = NodoPiso(nombre, R, C, F, S, patrones)
            lista_pisos.agregar(nuevo_piso)
        return lista_pisos
    except FileNotFoundError:
        print("El archivo especificado no existe.")
        return None

def generate_table(patron_data, R, C):
    table = ""
    for i in range(R):
        table += "<TR>"
        for j in range(C):
            color = '#FFFFFF' if patron_data[i * C + j] == 'B' else '#000000'
            table += f'<TD BGCOLOR="{color}"></TD>'
        table += "</TR>"
    return table

if __name__ == "__main__":
    print("Bienvenido a Pisos de Guatemala, S.A.")
    
    while True:
        filename = input("Ingrese el nombre del archivo XML: ")
        lista_pisos = read_xml(filename)
        print("Archivo leído correctamente")
        if lista_pisos is not None:
            break

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso_nodo = lista_pisos.buscar_piso(nombre_piso)
            if piso_nodo and piso_nodo.dato:   
                patron_data = None
                actual = piso_nodo.dato.patrones.cabeza 
                while actual:
                    codigo, data = actual.dato
                    if codigo == codigo_patron:
                        patron_data = data
                        break
                    actual = actual.siguiente
                if patron_data:
                    mostrar_patron(patron_data, piso_nodo.dato.R, piso_nodo.dato.C)
                else:
                    print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
            else:
                print("El nombre del piso ingresado no corresponde a ningún piso disponible.")
        
        elif opcion == "2":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso_nodo = lista_pisos.buscar_piso(nombre_piso)
            if piso_nodo and piso_nodo.dato:  
                seleccionar_codigo_patron(piso_nodo.dato)
            else:
                print("El nombre del piso ingresado no corresponde a ningún piso disponible.")
        
        elif opcion == "3":
            print()
            mostrar_pisos_y_patrones(lista_pisos)
        
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")
