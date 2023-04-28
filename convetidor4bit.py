import argparse
from pathlib import Path

from PIL import Image
import numpy as np
import time


def stringToHex(string: str):
    string = string.split()
    for i, valor in enumerate(string):
        string[i] = "0x"+valor
        string[i] = int(string[i], 16)
    return string


def funcPrimeraParte():
    inicio = time.time()
    primeraParte = "42 4D  96 00 00 00 00 00 00 00 76 00 00 00 28 00 00 00"
    primeraParte = stringToHex(primeraParte)
    fin = time.time()
    print(f"Tiempo primera parte: {fin-inicio}", end="\n\n")
    return primeraParte


def funcTamano(img: Image):
    inicio = time.time()
    tamano = []
    alto = hex(img.height)
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
        tamano[i] = int(tamano[i], 16)
    fin = time.time()
    print(f"Tiempo tamano: {fin-inicio}", end="\n\n")
    return tamano


def funcSegundaParte():
    inicio = time.time()

    segundaParte = "00 01 00 04  00 00 00 00 00 20 00  00 00 00 00  00 00 00 00  00 00 10 00 00 00 00 00  00 00"
    segundaParte = stringToHex(segundaParte)

    fin = time.time()
    print(f"Tiempo segunda parte: {fin-inicio}", end="\n\n")
    return segundaParte


def funcPaleta(img: Image):
    inicio = time.time()
    paleta = img.getpalette()
    paleta = paleta[:16*3]

    aux1 = []
    aux2 = []
    for i, valor in enumerate(paleta.copy()):
        aux1.append(valor)
        if((i+1) % 3 == 0):
            aux1.reverse()
            aux2.extend(aux1)
            aux1.clear()
    paleta = aux2

    aux = []
    for i, valor in enumerate(paleta.copy()):
        aux.append(valor)
        if ((i+1) % 3 == 0) and i != 0:
            aux.append(0)
    paleta = aux.copy()
    fin = time.time()
    print(f"Tiempo paleta: {fin-inicio}", end="\n\n")
    return paleta


def funcImagen(img: Image):
    inicio = time.time()
    imgArr = np.asarray(img)
    imgArr = imgArr.copy()
    imgArr = np.flip(imgArr)

    for i in range(len(imgArr)):
        imgArr[i] = np.flip(imgArr[i])
    imgArr = imgArr.flatten()

    aux1 = "0x"
    aux2 = []
    for i, valor in enumerate(imgArr):
        aux1 += str(hex(valor)[2:])
        if (i+1) % 2 == 0:
            aux2.append(int(aux1, 16))
            aux1 = "0x"
    imgArr = aux2.copy()
    fin = time.time()
    print(f"Tiempo imagen parte: {fin-inicio}", end="\n\n")
    return imgArr


def convertidor4Bit(img: Image, dest="archivo.bmp"):
    img = img.convert("P",
                      palette=Image.Palette.ADAPTIVE,
                      colors=16)

    primeraParte = funcPrimeraParte()

    tamano = funcTamano(img)

    segundaParte = funcSegundaParte()

    paleta = funcPaleta(img)

    imgArr = funcImagen(img)

    with open(dest, "wb") as f:
        f.write(bytearray(primeraParte))
        f.write(bytearray(tamano))
        f.write(bytearray(segundaParte))
        f.write(bytearray(paleta))
        f.write(bytearray(imgArr))


def process(args):
    outputPath = Path(args.output)
    outputPath.mkdir(exist_ok=True)
    imgPaths = []
    imgFoldersPaths = []
    for path in args.dirs:
        if(Path(path).is_file()):
            imgPaths.append(path)
            continue
        if(Path(path).is_dir()):
            imgFoldersPaths.append(path)
            continue
    
    for imgPath in imgPaths:
        with Image.open(imgPath) as img:
            convertidor4Bit(img,outputPath.joinpath(Path(imgPath).name))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='External tool example.')
    parser.add_argument('--dirs', required=True, type=str,
                        nargs='+', help='build folder path')
    parser.add_argument('--output', required=True, help='build folder path')

    args = parser.parse_args(['--dirs', 'graphics/tiles2_palette.bmp','graphics/tiles2_palette.bm','graphic','graphics', 'graphics/tiles2.bmp', "--output", "dirImagen"])
    process(args)
