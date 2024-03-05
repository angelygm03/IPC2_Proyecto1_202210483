import xml.etree.ElementTree as ET
from graphviz import Digraph
from NodoPiso import NodoPiso
from ListaPisos import ListaPisos
from ListaEnlazada import ListaEnlazada

def read_xml(filename):
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

if __name__ == "__main__":
    filename = input("Ingrese el nombre del archivo XML: ")
    lista_pisos = read_xml(filename)

    actual = lista_pisos.cabeza
    while actual:
        nombre_piso = actual.dato.nombre
        print(f"Piso: {actual.dato.nombre}")
        for codigo_patron, patron_data in actual.dato.patrones:
            R = actual.dato.R
            C = actual.dato.C
            generate_graphviz(patron_data, R, C, nombre_piso, codigo_patron, f'piso_{nombre_piso}_{codigo_patron}.png')
            print(f"- Código de Patrón: {codigo_patron}")
            print(f"  {patron_data}")
        actual = actual.siguiente
