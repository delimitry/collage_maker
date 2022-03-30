'''
pip install openpyxl

'''
import argparse
import csv
import os
from os import replace
import os.path
from PIL import Image
from PIL import ImageDraw
import matplotlib.pyplot as plt
from datetime import date
import argparse
from os import path 
from PIL import ImageFont
import openpyxl
from pathlib import Path
from re import sub

#global program vars
font_size = 50
font_color= 'black'
font_case = 'excel' # lower, upper, title, excel
font_type = 'arial.ttf'

imagePath = '' # NO MODIFICAR ESTOS VALORES
altNombre = 0 # NO MODIFICAR ESTOS VALORES
csvPath = '' # NO MODIFICAR ESTOS VALORES
nombreHoja = '' # NO MODIFICAR ESTOS VALORES
nombreCol = '' # NO MODIFICAR ESTOS VALORES

def use_fixed_params():
    global imagePath, altNombre, csvPath, nombreHoja, nombreCol
    imagePath = 'align.jpg'      #Cambiar el valor que esta entre '' en caso se ser necesario
    altNombre = 43              #Cambiar el valor en caso se ser necesario
    csvPath = 'lista.xlsx'       #Cambiar el valor que esta entre '' en caso se ser necesario
    nombreHoja = 'Hoja1'         #Cambiar el valor que esta entre '' en caso se ser necesario
    nombreCol = 'Preferred_Name' #Cambiar el valor que esta entre '' en caso se ser necesario

def get_params_from_user():
    print('  Capturando Parametros:')
    okflag = True

    while(okflag):
        global imagePath
        imagePath = input('    Cual es el nombre de la imagen para el diploma: ')
        if (path.exists(imagePath)):
            okflag = False
        else:
            print(f'      La imagen {imagePath} no existe')        
    
    okflag = True

    while(okflag):
        global altNombre
        altNombre = int(input('    Cual es el porcentaje de la altura (de arriba hacia abajo) a la que hay que colocar el nombre: '))
        if (altNombre>0 and altNombre<101):
            okflag = False
        else:
            print(f'      La altura debe ser entre 1 y 100')
    
    okflag = True
    
    while(okflag):
        global csvPath
        csvPath = input('    Cual es el nombre del csv con la lista de personas: ')
        if (path.exists(csvPath)):
            okflag = False
        else:
            print(f'     El archivo:  {csvPath} no existe')

    global nombreHoja
    nombreHoja = input('    Cual es el nombre de la hoja en el excel en donde estan los datos?: ')

    global nombreCol
    nombreCol = input('    Cual es el nombre de la columna donde estan los nombres en la hoja de excel: ')

    print('  Finalizando Captura de Parametros:')

def add_text_to_Image(personName, personNumber):

    #open image
    img = Image.open(imagePath)
    
    #Get image size
    #W,H = (829,649)
    W,H = img.size
    
    # Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    
    # Custom font style and font size
    myFont = ImageFont.truetype(font_type, font_size)

    w, h = I1.textsize(personName,font=myFont)
    
    I1.text(((W-w)/2,(altNombre/100*H)), personName, font=myFont, fill = font_color)
    
    #img.show()
    
    img.save(f'./output/{personName.replace(" ","_").replace(".","").strip()}.pdf')

    img.close()

    print(f'    Certificado #{personNumber} creado para: {personName}')

def read_names_from_file():
    print('  Iniciando Creacion de Certificados Individuales:')    
    
    personas = []

    xlsx_file = Path(csvPath)
    wb_obj = openpyxl.load_workbook(xlsx_file)
    nombres = wb_obj[nombreHoja]

    # Determinar # columna donde esta el titulo especificado
    index = 0
    columnFound = False 
    #Recorre todas las columnas de la fila 1 y compara el header
    for column in nombres.iter_cols(1, nombres.max_column):
        if (column[0].value ==nombreCol):
            columnFound = True
            break
        index = index +1

    if (columnFound):
        # identificar el tipo de case en la letra que se va a usar (minuscula, mayuscula, titulo, la que tiene el exel)
        # Luego, recorre todas las filas de la columna que tiene el header especifico y guarda sus valores en un directorio
        
        if (font_case == 'title'):
            for row in nombres.iter_rows(2, nombres.max_row):
                personas.append(row[index].value.title())
        elif (font_case == 'upper'):
            for row in nombres.iter_rows(2, nombres.max_row):
                personas.append(row[index].value.upper())
        elif (font_case == 'lower'):
            for row in nombres.iter_rows(2, nombres.max_row):
                personas.append(row[index].value.lower())
        else:
            for row in nombres.iter_rows(2, nombres.max_row):
                personas.append(row[index].value)

        # si el excel tiene datos en esa columna se generan los certificados
        if len(personas) >= 1:
            count = 1
            for persona in personas:
                add_text_to_Image(persona, count)
                count = count +1
        else:
            print(f'    No existen valores en la columna: {nombreCol} en la hoja {nombreHoja} del archivo de excel.')
        
    else: 
        print(f'    La columna: {nombreCol} no existe en la hoja {nombreHoja} del archivo de excel.')
    

    print('  Finalizando Creacion de Certificados Individuales:')

def main():
    print('Iniciando programa para crear certifiados....')

    # El simoblo # hace que las lineas en este archivo no se ejecuten.

    # Para usar los parametros desde este archivo:
        # debes quitar el # adelante de use_fixed_params() y ponerlo en read_names_from_file()
        # para modificar los parametors debes hacerlo a partir de la linea 36 a 40
     
    #Para que el sistema pregunte los parametros:  
        # debes quitar poner un # adelante de use_fixed_params() y quitarlo en read_names_from_file()

    use_fixed_params()
    #get_params_from_user()

    read_names_from_file()
    
    print('--------------fin----------------------')

if __name__ == '__main__':
    main()