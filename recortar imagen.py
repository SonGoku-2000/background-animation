from PIL import Image, ImageChops
import numpy as np
from converter4Bit import converter4Bit
import argparse
from pathlib import Path


def igual(img1: Image, img2: Image):
    diferencia = ImageChops.subtract_modulo(img1, img2)
    arr = np.asarray(diferencia)
    if (np.count_nonzero(arr) == 0):
        return True
    else:
        return False


def crearTiles(img: Image):
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
    frames.append(mapa.copy())
    mapa.clear()


def guardarTilemap(path="graphics/tiles2", bpp=4, compresion="none"):
    if (bpp == 4):
        colores = 16
    if (bpp == 8):
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
    tiles.clear()


def process(args: argparse.Namespace):
    global frames
    imgPaths = []
    imgFolderPaths = []
    dicImgPaths = {}

    for dir in args.dirs:

        if Path(dir).is_file():
            imgPaths.append(dir)
        elif Path(dir).is_dir():
            imgFolderPaths.append(dir)
        else:
            try:
                raise ValueError('File or path not exist')
            except ValueError:
                print(f"'{dir}' is not a real file or path")
                raise

    for path in imgPaths:
        aux = path.split("_")
        nombre = "_".join(aux[:-1])
        if dicImgPaths.get(nombre) == None:
            dicImgPaths[nombre] = []
        dicImgPaths[nombre].append(path)

    for nombre in dicImgPaths:
        dicImgPaths[nombre].sort()

    for ImgPaths in dicImgPaths:
        frames = []
        outputDir = Path(args.build).joinpath(ImgPaths)
        outputDir.parent.mkdir(exist_ok=True, parents=True)
        for imgPath in dicImgPaths[ImgPaths]:
            with Image.open(imgPath) as image:
                crearTiles(image)

        guardarTilemap(outputDir.__str__())


tiles = []
mapa = []
frames = []

debug = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='External tool example.')
    parser.add_argument('--build', "-b", required=False,
                        help='build folder path')
    parser.add_argument('--dirs', "-d", required=False,
                        type=str, nargs='+', help='build folder path')
    args = parser.parse_args(['-d', "animacion/tiles2_0.bmp", "animacion/tiles2_2.bmp", "animacion/tiles2_1.bmp",
                             "animacion/tiles_0.bmp", "animacion/mapa_0.bmp", "animacion/tiles_2.bmp", "animacion/tiles_1.bmp", "-b", "build"])
    process(args)
    tiles.clear()
    mapa.clear()
