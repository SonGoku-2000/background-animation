import png
import numpy as np
from PIL import Image

with Image.open('a.bmp') as image:

    # convert RGB to 16 colors
    image = image.quantize(16)

    # get palette as flat list [r, g, b, r, g, b, ...]
    palette = image.getpalette()
    # conver flat list to tupled [(r, g, b), (r, g, b), ...]
    palette = [tuple(palette[x:x+3]) for x in range(0, len(palette), 3)]
    #print(len(palette))
    palette = palette[:16]
    print(palette)

    # get pixels/indexes as numpy array
    im = np.array(image)
    print(im)

    with open('png-4bpp.png', 'wb') as f:
        #png_writer = png.Writer(im.shape[1], im.shape[0], bitdepth=4)  # without palette
        png_writer = png.Writer(im.shape[1], im.shape[0], bitdepth=4, palette=palette)  # with palette
        png_writer.write(f, im)