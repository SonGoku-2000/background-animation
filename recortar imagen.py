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
    return alto, ancho


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

    includeFolderPath = Path(args.build).joinpath("include")
    includeFolderPath.mkdir(exist_ok=True, parents=True)
    srcFolderPath = Path(args.build).joinpath("src")
    srcFolderPath.mkdir(exist_ok=True, parents=True)

    for animacionName in dicImgPaths:
        frames = []
        outputDir = Path(args.build).joinpath(animacionName)
        outputDir.parent.mkdir(exist_ok=True, parents=True)
        for imgPath in dicImgPaths[animacionName]:
            with Image.open(imgPath) as image:
                alto,ancho = crearTiles(image)

        guardarTilemap(outputDir.__str__())

        output_header_path = outputDir.__str__() + ".hpp"
        output_cpp_path = outputDir.__str__() + ".cpp"
        print(animacionName)
        with open(output_header_path, 'w') as output_header:
            output_header.write(f'#ifndef {outputDir.name.upper()}_HPP \n')
            output_header.write(f'#define {outputDir.name.upper()}_HPP \n')
            output_header.write('\n')
            output_header.write('#include "bn_memory.h" \n')
            output_header.write('#include "bn_regular_bg_ptr.h" \n')
            output_header.write('#include "bn_regular_bg_item.h" \n')
            output_header.write('#include "bn_regular_bg_map_ptr.h" \n')
            output_header.write('#include "bn_regular_bg_map_cell_info.h" \n')
            output_header.write(
                f'#include "bn_regular_bg_tiles_items_{outputDir.name}.h" \n')
            output_header.write(
                f'#include "bn_bg_palette_items_{outputDir.name}_palette.h" \n')
            output_header.write('namespace bn { \n')
            output_header.write('   namespace animation { \n')
            for i, frame in enumerate(frames):
                output_header.write(
                    f'        constexpr bn::regular_bg_map_cell frame{i}[] = {"{"} \n')
                output_header.write(f'          {str(frame)[1:-1]}\n')
                output_header.write('        }; \n')

            output_header.write('\n')
            output_header.write('       struct Animation { \n')
            output_header.write(f'            static constexpr int columns = {ancho}; \n')
            output_header.write(f'            static constexpr int rows = {alto}; \n')
            output_header.write('            static constexpr int cells_count = columns * rows; \n')
            output_header.write('\n')
            output_header.write('            int wait; \n')
            output_header.write('\n')
            output_header.write('            int cont = 1; \n')
            output_header.write('\n')
            output_header.write('            int frameActual = 0; \n')
            output_header.write('\n')
            output_header.write(f'            int framesTotales = {len(frames)}; \n')
            output_header.write('\n')
            output_header.write('            Animation(int wait_updates); \n')
            output_header.write('\n')
            output_header.write('            alignas(int) bn::regular_bg_map_cell cells[cells_count]; \n')
            output_header.write('            bn::regular_bg_map_item map_item; \n')
            output_header.write('\n')
            output_header.write('            bn::regular_bg_item bg_item; \n')
            output_header.write('\n')
            output_header.write('            bn::regular_bg_ptr bg; \n')
            output_header.write('\n')
            output_header.write('            bn::regular_bg_map_ptr bg_map; \n')
            output_header.write('\n')
            output_header.write('            void update(); \n')
            output_header.write('\n')
            output_header.write('            void reset(); \n')
            output_header.write('        }; \n')
            output_header.write('    } \n')
            output_header.write('} \n')
            output_header.write('#endif' + '\n')
            output_header.write('\n')



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
                             "animacion/tiles_0.bmp", "animacion/mapa_0.bmp", "animacion/tiles_2.bmp", "animacion/tiles_1.bmp", "-b", "external_tool"])
    process(args)
    tiles.clear()
    mapa.clear()
