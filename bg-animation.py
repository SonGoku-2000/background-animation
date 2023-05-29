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

    paleta = tilemap.crop((0, 0, 8, 8))
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
    if args.compression not in ("none", "lz77", "run_length", "huffman", "auto"):
        try:
            raise ValueError('Compression method not valid')
        except ValueError:
            print(f"'{args.compression}' is not a valid compresion method.")
            raise

    if args.bpp not in (4, 8):
        try:
            raise ValueError('bpp not valid')
        except ValueError:
            print(f"'{args.bpp}' is not a valid bpp value.")
            raise

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
        nombre = Path(nombre).name
        if dicImgPaths.get(nombre) == None:
            dicImgPaths[nombre] = []
        dicImgPaths[nombre].append(path)

    for folder in imgFolderPaths:
        for path in Path(folder).iterdir():
            path = path.__str__()
            aux = path.split("_")
            nombre = "_".join(aux[:-1])
            nombre = Path(nombre).name
            if dicImgPaths.get(nombre) == None:
                dicImgPaths[nombre] = []
            dicImgPaths[nombre].append(path)

    for nombre in dicImgPaths:
        dicImgPaths[nombre].sort()

    outputIncludeFolderPath = Path(args.build).joinpath("include")
    outputIncludeFolderPath.mkdir(exist_ok=True, parents=True)
    outputSrcFolderPath = Path(args.build).joinpath("src")
    outputSrcFolderPath.mkdir(exist_ok=True, parents=True)
    outputGraphicsForderPath = Path(args.build).joinpath("graphics")
    outputGraphicsForderPath.mkdir(exist_ok=True, parents=True)

    for animacionName in dicImgPaths:
        if (args.verbose):
            print(f'Procesing animation: "{animacionName}"')

        frames = []
        outputGraphicsDir = outputGraphicsForderPath.joinpath(animacionName)
        for imgPath in dicImgPaths[animacionName]:
            if (args.verbose):
                print(f'Procesing file: "{imgPath}"')
            with Image.open(imgPath) as image:
                alto, ancho = crearTiles(image)

        guardarTilemap(outputGraphicsDir.__str__(), args.bpp, args.compression)

        output_header_path = outputIncludeFolderPath.joinpath(
            animacionName).__str__() + ".hpp"
        output_cpp_path = outputSrcFolderPath.joinpath(
            animacionName).__str__() + ".cpp"

        if (args.verbose):
            print(f'Procesing header file: "{output_header_path}"')

        with open(output_header_path, 'w') as output_header:
            output_header.write(f'#ifndef {animacionName.upper()}_HPP \n')
            output_header.write(f'#define {animacionName.upper()}_HPP \n')
            output_header.write('\n')
            output_header.write('#include "bn_memory.h" \n')
            output_header.write('#include "bn_regular_bg_ptr.h" \n')
            output_header.write('#include "bn_regular_bg_item.h" \n')
            output_header.write('#include "bn_regular_bg_map_ptr.h" \n')
            output_header.write('#include "bn_regular_bg_map_cell_info.h" \n')
            output_header.write(
                f'#include "bn_regular_bg_tiles_items_{animacionName}.h" \n')
            output_header.write(
                f'#include "bn_bg_palette_items_{animacionName}_palette.h" \n')
            output_header.write('\n')
            output_header.write('namespace bn { \n')
            output_header.write('    namespace animation { \n')
            output_header.write(
                f'        namespace {animacionName}_data {"{"} \n')
            for i, frame in enumerate(frames):
                output_header.write(
                    f'            constexpr bn::regular_bg_map_cell frame{i}[] = {"{"} \n')
                output_header.write(f'               {str(frame)[1:-1]}\n')
                output_header.write('            }; \n')
            output_header.write('        }\n')

            output_header.write('\n')
            output_header.write(f'       struct {animacionName} {"{"} \n')
            output_header.write(
                f'            static constexpr int columns = {ancho}; \n')
            output_header.write(
                f'            static constexpr int rows = {alto}; \n')
            output_header.write(
                '            static constexpr int cells_count = columns * rows; \n')
            output_header.write('\n')
            output_header.write('            int wait; \n')
            output_header.write('\n')
            output_header.write('            int cont = 1; \n')
            output_header.write('\n')
            output_header.write('            int frameActual = 0; \n')
            output_header.write('\n')
            output_header.write(
                f'            int framesTotales = {len(frames)}; \n')
            output_header.write('\n')
            output_header.write(
                f'            {animacionName}(int wait_updates); \n')
            output_header.write('\n')
            output_header.write(
                '            alignas(int) bn::regular_bg_map_cell cells[cells_count]; \n')
            output_header.write(
                '            bn::regular_bg_map_item map_item; \n')
            output_header.write('\n')
            output_header.write('            bn::regular_bg_item bg_item; \n')
            output_header.write('\n')
            output_header.write('            bn::regular_bg_ptr bg; \n')
            output_header.write('\n')
            output_header.write(
                '            bn::regular_bg_map_ptr bg_map; \n')
            output_header.write('\n')
            output_header.write('            void update(); \n')
            output_header.write('\n')
            output_header.write('            void reset(); \n')
            output_header.write('        }; \n')
            output_header.write('    } \n')
            output_header.write('} \n')
            output_header.write('#endif' + '\n')
            output_header.write('\n')

        if (args.verbose):
            print("Header file writen")

        if (args.verbose):
            print(f'Procesing src file: "{output_cpp_path}"')

        with open(output_cpp_path, 'w') as output_cpp:
            output_cpp.write(f'#include "{animacionName}.hpp" \n')
            output_cpp.write('\n')
            output_cpp.write('namespace bn { \n')
            output_cpp.write('    namespace animation { \n')
            output_cpp.write('\n')
            output_cpp.write(
                f'        {animacionName}::{animacionName}(int wait_updates) : \n')
            output_cpp.write(
                '            map_item(cells[0], bn::size(columns, rows)), \n')
            output_cpp.write(
                f'            bg_item(bn::regular_bg_tiles_items::{animacionName}, \n')
            output_cpp.write(
                f'                    bn::bg_palette_items::{animacionName}_palette, \n')
            output_cpp.write('                    map_item), \n')
            output_cpp.write('            bg(bg_item.create_bg(0, 0)), \n')
            output_cpp.write('            bg_map(bg.map()) { \n')
            output_cpp.write('\n')
            output_cpp.write('            wait = wait_updates; \n')
            output_cpp.write('            bg_map.reload_cells_ref(); \n')
            output_cpp.write('        } \n')
            output_cpp.write('\n')
            output_cpp.write(
                f'        void {animacionName}::update() {"{"} \n')
            output_cpp.write('            if (cont < wait) { \n')
            output_cpp.write('                cont++; \n')
            output_cpp.write('                return; \n')
            output_cpp.write('            } \n')
            output_cpp.write('            cont = 1; \n')
            output_cpp.write('\n')

            for i in range(len(frames)):
                if i == 0:
                    output_cpp.write('            if (frameActual == 0) { \n')
                    output_cpp.write(
                        f'                bn::memory::copy({animacionName}_data::frame0[0], cells_count, cells[0]); \n')
                    output_cpp.write('            } \n')
                    continue

                output_cpp.write(
                    f'            else if (frameActual == {i}) {"{"} \n')
                output_cpp.write(
                    f'                bn::memory::copy({animacionName}_data::frame{i}[0], cells_count, cells[0]); \n')
                output_cpp.write('            } \n')
            output_cpp.write('\n')
            output_cpp.write('            frameActual++; \n')
            output_cpp.write('\n')
            output_cpp.write(
                '            if (frameActual > framesTotales) { \n')
            output_cpp.write('                frameActual = 0; \n')
            output_cpp.write('            } \n')
            output_cpp.write('\n')
            output_cpp.write('            bg_map.reload_cells_ref(); \n')
            output_cpp.write('        } \n')
            output_cpp.write('\n')
            output_cpp.write(f'        void {animacionName}::reset() {"{"} \n')
            output_cpp.write(
                f'            bn::memory::copy({animacionName}_data::frame0[0], cells_count, cells[0]); \n')
            output_cpp.write('        } \n')
            output_cpp.write('    } \n')
            output_cpp.write('} \n')

        if (args.verbose):
            print("Src file writen\n\n")


tiles = []
mapa = []
frames = []

debug = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='External tool example.')
    parser.add_argument('--build', "-b", required=True,
                        help='build folder path')
    parser.add_argument('--dirs', "-d", required=True,
                        type=str, nargs='+', help='Dirs for images or folder with images')
    parser.add_argument('--compression', "-c", default="none", required=False,
                        type=str, help='Compression method')
    parser.add_argument('--bpp', '--bpp_mode', default=4,
                        type=int, help='bpp mode for the color palette')
    parser.add_argument('--verbose', '-v', action='store_true')

    args = parser.parse_args(['-b','external_tool','-d','animacion'])
    process(args)
    tiles.clear()
    mapa.clear()
