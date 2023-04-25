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
                if igual(tile,tileActual):
                    mapa.append(id)
                    break
            else:
                mapa.append(len(tiles))
                tiles.append(tileActual)

tiles = []
mapa = []

with Image.open("animacion/mapa_prueba.bmp") as img:
    b = img.crop((0, 0, 8, 8))
    c = img.crop((8, 0, 16, 8))
    
    inicio = time.time()
    crearTiles(img)
    fin = time.time()
    print(fin-inicio)
    
    cont = 0
    print(len(tiles))

    tilemap = Image.new(mode="RGB",size=(len(tiles) * 8,8))
    for i, tile in enumerate(tiles):
        tilemap.paste(tile,((i*8),0))
    tilemap = tilemap.convert("P", palette=Image.Palette.ADAPTIVE, colors=16)
    tilemap.save("graphics/tiles2.bmp")

    for i, id in enumerate(mapa):
        if i % 16 == 0:
            print()
        print(id, end=",")
    print()

print(1024**0.5)
