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


def funcFirstPart(debug):
    inicio = time.time()
    primeraParte = "42 4D  96 00 00 00 00 00 00 00 76 00 00 00 28 00 00 00"
    primeraParte = stringToHex(primeraParte)
    fin = time.time()
    if debug:
        print(f"Time first part: {fin-inicio}", end="\n\n")
    return primeraParte


def funcSize(img: Image, debug):
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
    if debug:
        print(f"Time size: {fin-inicio}", end="\n\n")
    return tamano


def funcSecondPart(debug):
    inicio = time.time()

    segundaParte = "00 01 00 04  00 00 00 00 00 20 00  00 00 00 00  00 00 00 00  00 00 00 00 00 00 00 00  00 00"
    segundaParte = stringToHex(segundaParte)

    fin = time.time()
    if debug:
        print(f"Time second part: {fin-inicio}", end="\n\n")
    return segundaParte


def funcPalette(img: Image, debug):
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
    if debug:
        print(f"Time palette: {fin-inicio}", end="\n\n")
    return paleta


def funcImage(img: Image.Image, debug):
    inicio = time.time()
    imgArr = np.asarray(img)
    imgArr = np.flip(imgArr)

    if img.width <= 16:
        nCeros = 1

        while img.width > nCeros:
            nCeros *= 2
    else:
        cont = 2
        nCeros = 16
        while img.width > nCeros:
            cont += 1
            nCeros = 8 * cont

    nCeros = nCeros - img.width
    aux = []
    for i in range(len(imgArr)):
        aux.extend(np.flip(imgArr[i]).tolist())
        aux.extend([0 for i in range(nCeros)])

    imgArr = aux

    aux1 = "0x"
    aux2 = []
    for i, valor in enumerate(imgArr):
        aux1 += str(hex(valor)[2:])
        if (i+1) % 2 == 0:
            aux2.append(int(aux1, 16))
            aux1 = "0x"
    imgArr = aux2.copy()
    fin = time.time()
    if debug:
        print(f"Time image part: {fin-inicio}", end="\n\n")
    return imgArr


def converter4Bit(img: Image, dest="archivo.bmp", quantize=False, debug=False):
    """
    Parameters
    ----------
    img : Image
        The image that be to convert to 4bpp image
    dest : str, default "archivo.bmp"
        The name of the  output image
    quantize : bool, False
        Use pillow's quantize method instead of convert method for reduce colors
    debug : bool, default False
        Print the steps and the progres of the conversion
    """

    if quantize:
        img = img.quantize(16)
    else:
        img = img.convert("P",
                          palette=Image.Palette.ADAPTIVE,
                          colors=16)

    primeraParte = funcFirstPart(debug)

    tamano = funcSize(img, debug)

    segundaParte = funcSecondPart(debug)

    paleta = funcPalette(img, debug)

    imgArr = funcImage(img, debug)

    with open(dest, "wb") as f:
        f.write(bytearray(primeraParte))
        f.write(bytearray(tamano))
        f.write(bytearray(segundaParte))
        f.write(bytearray(paleta))
        f.write(bytearray(imgArr))


def process(args: argparse.Namespace):
    """
    Parameters
    ----------
    args : argsparse
           argsparse that contains the folowing args:\n
           dirs: [str, str, ...], 
           output: str, 
           verbose: bool, 
           progress: bool,
           quantize: bool
    """

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
        if args.verbose:
            print("Processing:", imgPath, end="\n\n")

        with Image.open(imgPath) as img:
            converter4Bit(img, outputPath.joinpath(Path(imgPath).stem + ".bmp"),
                          args.quantize,
                          args.progress)

    for imgForderPath in imgFoldersPaths:
        for imgPath in Path(imgForderPath).glob("*.*"):
            if (imgPath.suffix.lower() not in [".bmp", ".png", ".jpg", ".jpeg"]):
                continue

            if args.verbose:
                print("Processing:", imgPath, end="\n\n")

            outputPath.joinpath(imgForderPath).mkdir(exist_ok=True)
            with Image.open(imgPath) as img:
                converter4Bit(img, outputPath.joinpath(imgForderPath).joinpath(imgPath.stem + ".bmp"),
                              args.quantize,
                              args.progress)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converter for 8bit bmp to 4bit bmp, that is similar to the usenti output.',
                                     epilog="This is not too eficient and could be improbed, but works.")
    parser.add_argument('--dirs', '-d', required=True, type=str, nargs='+',
                        help='Relative paths for images or folders with images to convert, separed with a space ex: --dirs img1.bmp path1/')
    parser.add_argument('--output', '-o', required=True,
                        help='Output folder for the images.')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--progress', '-p',  action='store_true')
    parser.add_argument('-q', '--quantize', action='store_true',
                        help="Use pillow's quantize method instead of convert method for reduce colors")
    args = parser.parse_args()
    process(args)
