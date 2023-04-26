from PIL import Image, ImageChops
import numpy as np
import time


def igual(img1, img2):
    diferencia = ImageChops.subtract_modulo(img1, img2)
    arr = np.asarray(diferencia)
    if(np.count_nonzero(arr) == 0):
        return True
    else:
        return False


def crearTiles(img):
    alto = img.height//8
    ancho = img.width//8

    for i in range(alto):
        for j in range(ancho):

            tileActual = img.crop((j*8, i*8, (j*8)+8, (i*8)+8))
            if len(tiles) == 0:
                tiles.append(tileActual)

            for id, tile in enumerate(tiles):
                if igual(tile, tileActual):
                    mapa.append(id)
                    break
            else:
                mapa.append(len(tiles))
                tiles.append(tileActual)


def guardarTilemap(path="graphics/tiles2", bpp=4, compresion="none"):
    if(bpp == 4):
        colores = 16
    if(bpp == 8):
        colores = 256

    tilemap = Image.new(mode="RGB", size=(len(tiles) * 8, 8))
    for i, tile in enumerate(tiles):
        tilemap.paste(tile, ((i*8), 0))
    tilemap = tilemap.convert(
        "P", palette=Image.Palette.ADAPTIVE, colors=colores)
    tilemap.save(path+".bmp")

    with open(path + '.json', 'w') as archivoJson:
        archivoJson.write('{\n')
        archivoJson.write('    "type": "regular_bg_tiles",\n')
        archivoJson.write(f'    "bpp_mode": "bpp_{bpp}",\n')
        archivoJson.write(f'    "compression": "{compresion}"\n')
        archivoJson.write('}\n')

    paleta = tiles[0]
    paleta = paleta.convert(
        "P", palette=Image.Palette.ADAPTIVE, colors=colores)
    paleta.save(path+"_palette.bmp")

    with open(path + '_palette.json', 'w') as archivoJson:
        archivoJson.write('{\n')
        archivoJson.write('    "type": "bg_palette",\n')
        archivoJson.write(f'    "bpp_mode": "bpp_{bpp}",\n')
        archivoJson.write(f'    "colors_count": {colores}\n')
        archivoJson.write('}\n')


tiles = []
mapa = []

debug = False
"""
42 4D 96 00  00 00 00 00  00 00 76 00  00 00 28 00  
00 00                                          
      10 00  00 tamano imagen 1ro 2do 3ro 
                00  espacio
                    08 00 00 tamano imagen1ro 2do 3ro 
                             00 01 00 04  00 00 00  ni idea
00 00 20 00  00 00 00 00  00 00 00 00  00 00 10 00  ni idea
00 00 00 00  00 00 ni idea

1ro 2do 3ro 

paleta

                   FF FF  00 00 00 00  00 00 31 39  
66 00 30 6F  8A 00 3B 56  8F 00 11 11  11 00 33 33  
33 00 55 55  55 00 00 00  00 00 00 00  00 00 00 00  
00 00 00 00  00 00 00 00  00 00 00 00  00 00 00 00  
00 00 FF FF  FF 00

imagen 
ultimopixel 
primerpixel

"""

'''with open("imagen4bit.bmp","rb") as img:
    datos1 =  str(img.readline())
    datos1 = datos1.split("\\")
    for i,valor in enumerate(datos1):
        if (i%8 ==0):
            print()
        print(valor,end=" ")

print()'''

"""with open("tiles2.bmp","b+r") as img:
    datos2 =  str(img.readline())

    for i,valor in enumerate(datos2[4:]):
        if (i%16 ==0):
            print()
        print(valor,end="")"""
print()

#with open("graphics/tiles2_palette.bmp","b+r") as img:
#    print(img.readlines())

with Image.open("graphics/tiles2_palette.bmp") as img:
    arr = np.asarray(img)
    #print(arr)
    #print(img.getpalette()[:16*3])

    primeraParte = "42 4D  96 00 00 00 00 00 00 00 76 00 00 00 28 00 00 00"
    primeraParte = primeraParte.split()

    for i, valor in enumerate(primeraParte):
        primeraParte[i] = "0x"+valor
        primeraParte[i] = int(primeraParte[i],16)
    print(int("0x100",16))

    tamano = []

    alto = hex(img.height)
    alto = hex(255)
    alto = alto[2:]
    
    if len(alto) < 6:
        alto = f"{'0'*(6-len(alto))}{alto}"

    aux = ""
    for i, letra in enumerate(alto):
        aux += letra
        if i != 0 and (i+1) % 2 == 0:
            tamano.append(aux)
            aux = ""
    tamano.append("00")

    ancho = hex(img.width)
    ancho = ancho[2:]

    if len(ancho) < 6:
        ancho = f"{'0'*(6-len(ancho))}{ancho}"

    aux = ""
    for i, letra in enumerate(ancho):
        aux += letra
        if i != 0 and (i+1) % 2 == 0:
            tamano.append(aux)
            aux = ""
    tamano.reverse()

    for i, valor in enumerate(tamano):
        tamano[i] = "0x"+valor
        tamano[i] = int(tamano[i],16)


    segundaParte = "00 01 00 04  00 00 00 00 00 20 00  00 00 00 00  00 00 00 00  00 00 10 00 00 00 00 00  00 00"
    segundaParte = segundaParte.split()

    for i, valor in enumerate(segundaParte):
        segundaParte[i] = "0x"+valor
        segundaParte[i] = int(segundaParte[i],16)
    
    print(segundaParte)

    num = [int("0xff",16)]
    with open("archivo.bmp","wb") as f:
        f.write(bytearray(primeraParte))
        f.write(bytearray(tamano))
        f.write(bytearray(segundaParte))
    """b = img.crop((0, 0, 8, 8))
    c = img.crop((8, 0, 16, 8))

    inicio = time.time()
    crearTiles(img)
    fin = time.time()
    guardarTilemap()
    print(fin-inicio)

    cont = 0
    print(len(tiles))

    if debug:
        for i, id in enumerate(mapa):
            if i % 16 == 0:
                print()
            print(id, end=",")
    print()
    print(f"Tiles totales: {len(tiles)}")"""
