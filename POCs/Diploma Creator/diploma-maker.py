'''
Need to install this library:  pip install openpyxl

Exaple of the required config.json:

{    
    "Input": {
        "pedirValores" : false
    },
    "Imagen": {
        "nombreImagen" : "align.jpg",
        "PorcentajeAltNombre" : 43
    },
    "Excel": {
        "nombreArchivo" : "lista.xlsx",
        "nombreHoja" : "Hoja1",
        "nombreColumna" : "Preferred_Name"
    },
    "Letra": {
        "tamanno" : 36,
        "color": "black",
        "tipo" : "arial.ttf",
        "case" : "excel"
    }
}

'''
import openpyxl
import os
import os.path
from os import path
from os import replace
from pathlib import Path
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import json

#Reading global properties from json file
with open('config.json') as f:
        data = json.load(f)
        # Input
        pedirValores = data['Input']['pedirValores']
        # imagen
        imagePath = data['Imagen']['nombreImagen']
        altNombre = data['Imagen']['PorcentajeAltNombre']
        # Excel
        csvPath = data['Excel']['nombreArchivo']
        nombreHoja = data['Excel']['nombreHoja']
        nombreCol = data['Excel']['nombreColumna']
        # Letra
        font_size = data['Letra']['tamanno']
        font_color= data['Letra']['color']
        font_type = data['Letra']['tipo']
        font_case = data['Letra']['case']

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
                if (row[index].value != None):
                    personas.append(row[index].value.title())
        elif (font_case == 'upper'):
            for row in nombres.iter_rows(2, nombres.max_row):
                if (row[index].value != None):
                    personas.append(row[index].value.upper())
        elif (font_case == 'lower'):
            for row in nombres.iter_rows(2, nombres.max_row):
                if (row[index].value != None):
                    personas.append(row[index].value.lower())
        else:
            for row in nombres.iter_rows(2, nombres.max_row):
                if (row[index].value != None):
                    personas.append(row[index].value)

        # si el excel tiene datos en esa columna se generan los certificados
        if (len(personas) >= 1):
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
    print('Iniciando programa para crear diplomas....')

    if (pedirValores):
        get_params_from_user()

    read_names_from_file()
    
    print('--------------fin----------------------')

if __name__ == '__main__':
    main()