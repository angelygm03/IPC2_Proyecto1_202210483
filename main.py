import xml.etree.ElementTree as ET
from graphviz import Digraph
from NodoPiso import NodoPiso
from ListaPisos import ListaPisos
from ListaEnlazada import ListaEnlazada

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
    for codigo, patron in piso.patrones:
        if codigo == codigo_patron:
            patron_data = patron
            break
    
    if patron_data is None:
        print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
        return
    
    nuevo_codigo = input("Ingrese el nuevo código de patrón: ")
    costo, instrucciones = calcular_costo_minimo(patron, patron_data, piso.S, piso.F)

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

def mostrar_pisos_y_patrones(lista_pisos):
    actual = lista_pisos.cabeza
    while actual:
        piso = actual.dato
        print(f"Piso: {piso.nombre}")
        print("Códigos de patrones disponibles:")
        for codigo, _ in sorted(piso.patrones, key=lambda x: x[0]):
            print(f"- Código: {codigo}")
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
            patrones = []
            for patron in piso.find('patrones').findall('patron'):
                codigo = patron.get('codigo')
                patron_data = patron.text.strip()
                patrones.append((codigo, patron_data))
            nuevo_piso = NodoPiso(nombre, R, C, F, S, patrones)
            lista_pisos.agregar(nuevo_piso)
        return lista_pisos
    except FileNotFoundError:
        print("El archivo especificado no existe.")
        return None

def generate_graphviz(patron_data, R, C, nombre_piso, codigo_patron, file_name):
    dot = Digraph(comment=f'Piso: {nombre_piso} - Código: {codigo_patron}')
    dot.node('tab', label=f'<<TABLE>{generate_table(patron_data, R, C)}</TABLE>>', shape='none')
    dot.render(file_name, format='png', cleanup=True)

def generate_table(patron_data, R, C):
    table = ""
    for i in range(R):
        table += "<TR>"
        for j in range(C):
            color = '#FFFFFF' if patron_data[i * C + j] == 'B' else '#000000'
            table += f'<TD BGCOLOR="{color}"></TD>'
        table += "</TR>"
    return table

def calcular_costo_minimo(patron_origen, patron_destino, F, S):
    costo = 0
    instrucciones = []

    for i in range(len(patron_origen)):
        if patron_origen[i] != patron_destino[i]:
            if costo + F <= S:
                costo += F
                instrucciones.append(f"Voltear el azulejo en la posición {i + 1}")
            else:
                costo += S
                instrucciones.append(f"Intercambiar el azulejo en la posición {i + 1} con el siguiente")

    return costo, instrucciones

if __name__ == "__main__":
    print("Bienvenido a Pisos de Guatemala, S.A.")
    
    while True:
        filename = input("Ingrese el nombre del archivo XML: ")
        lista_pisos = read_xml(filename)
        if lista_pisos is not None:
            break

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso = lista_pisos.buscar_piso(nombre_piso)
            if piso:
                patron_data = next((patron_data for codigo, patron_data in piso.patrones if codigo == codigo_patron), None)
                if patron_data:
                    mostrar_patron(patron_data, piso.R, piso.C)
                else:
                    print("El código de patrón ingresado no corresponde a ningún patrón disponible.")
            else:
                print("El nombre del piso ingresado no corresponde a ningún piso disponible.")
        
        elif opcion == "2":
            nombre_piso = input("Ingrese el nombre del piso: ")
            codigo_patron = input("Ingrese el código del patrón: ")
            piso = lista_pisos.buscar_piso(nombre_piso)
            if piso:
                seleccionar_codigo_patron(piso)
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