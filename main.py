import xml.etree.ElementTree as ET
from graphviz import Digraph
from NodoPiso import NodoPiso
from ListaPisos import ListaPisos

def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    lista_pisos = ListaPisos()
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
        lista_pisos.agregar_piso(nombre, R, C, F, S, patrones)
    return lista_pisos

def generate_graphviz(pisos):
    actual = pisos.cabeza
    while actual:
        nombre = actual.nombre
        R = actual.R
        C = actual.C
        patrones = actual.patrones
        for patron in patrones:
            codigo, patron_data = patron
            dot = Digraph(comment=f'Piso: {nombre} - Código: {codigo}')
            dot.node('tab', label=f'<<TABLE>{generate_table(patron_data, R, C)}</TABLE>>', shape='none')
            dot.render(f'piso_{nombre}_{codigo}', format='png', cleanup=True)
        actual = actual.siguiente

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
    pisos = read_xml(filename)
    generate_graphviz(pisos)