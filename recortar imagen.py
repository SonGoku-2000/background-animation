from PIL import Image, ImageChops
import numpy as np
from convetidor4bit import convertidor4Bit


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

print()


with Image.open("graphics/tiles2.bmp") as img:
    convertidor4Bit(img)

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
