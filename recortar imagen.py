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


tiles = []
mapa = []

with Image.open("animacion/mapa_prueba.bmp") as img:
    alto = img.height//8
    ancho = img.width//8

    for i in range(alto):
        for j in range(ancho):

            tileActual = img.crop((j*8, i*8, (j*8)+8, (i*8)+8))
            if len(tiles) == 0:
                tiles.append(tileActual)

            for id, tile in enumerate(tiles):
                if igual(tile,tileActual):
                    print("coincidencia")
                    break
            else:
                tiles.append(tileActual)
            #tileActual.save(f"imagenes/{i}-{j}.bmp")

    b = img.crop((0, 0, 8, 8))
    c = img.crop((8, 0, 16, 8))
    inicio = time.time()
    z = igual(img, img)
    fin = time.time()
    print(fin-inicio)
