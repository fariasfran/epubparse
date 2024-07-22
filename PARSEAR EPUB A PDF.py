#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 18:19:52 2024

@author: teckla
"""

from bs4 import BeautifulSoup
# tambien necesitamos 'xml' para parsear el indice.

direc = '../LIBROS/OCIO/DUNE EPUB DESCOMPRIMIDO/'

### primero obtenemos el indice

with open(direc + 'OEBPS/content.opf', 'r') as file:
    indice = file.read()
soup = BeautifulSoup(indice, "xml")
indice = soup.find('spine')

### truncamos solo lo necesario. en este caso es desde "portadilla"
### hasta "x1_Notas_cartograficas_0005_0006.xhtml"

indice = indice.findAll('itemref')
indice_lista = []
for e in indice:
    nombre_archivo_xml = str(e).split('"')[1]
    if nombre_archivo_xml[0] == 'x':
        nombre_archivo_xml = nombre_archivo_xml[1:]
    indice_lista.append(nombre_archivo_xml)


indice_lista = indice_lista[6:65] #truncamos


#%%
### Probamos con un archivo y vemos qué sale.
archivo1 = indice_lista[2]
archivo2 = indice_lista[3]
direc += 'OEBPS/Text/' #ojo que si ejectuas estos mas de una vez se corrompe

with open(direc + archivo1, 'r') as file:
    archivo1 = file.read()
soup1 = BeautifulSoup(archivo1, "xml")

with open(direc + archivo2, 'r') as file:
    archivo2 = file.read()
soup2 = BeautifulSoup(archivo2, "xml")


### insertamos para el salto de pagina al exportar a pdf:
### <div style = "display:block; clear:both; page-break-after:always;"></div>
salto_pagina = '\n\n<div style = "display:block; clear:both; page-break-after:always;"></div>\n\n'

### .findChildren(recursive=False) permite quedarnos con el contenido del body
###  sin el tag No es necesario igual porque se interpretan como tags y ya.
archivo = soup1.find('body')

soup1.find('head')
soup2.find('body')

soup1.find('<html>')


### NOTA: AGREGAR UNA PAGINA EN BLANCO LUEGO DE LA PORTADA
###

with open(direc + 'output.xhtml', "w") as file:
    file.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">')
    file.write(str( soup1.find('head') ))
    file.write('\n\n')
    file.write(str( soup1.find('body') ))
    file.write(salto_pagina)
    file.write(str( soup2.find('head') ))
    file.write(str( soup2.find('body') ))
    file.write('</html>')

#%%
direc = '../LIBROS/OCIO/DUNE EPUB DESCOMPRIMIDO/OEBPS/Text/'
### el encabezado debe tener
with open(direc + 'output.xhtml', "w") as output:
    output.write('''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="es">
\n''')
    
    for e in indice_lista:
        with open(direc + e, 'r') as file:
            archivo = file.read()
            soup = BeautifulSoup(archivo, "xml")
        output.write(str( soup.find('head') ))
        output.write('\n\n')
        output.write(str( soup.find('body') ))
        output.write(salto_pagina)
    
    output.write('</html>')


