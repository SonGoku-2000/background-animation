from PIL import Image,ImageChops
import numpy as np

def igual(img1,img2):
    img1.show()
    img2.show()
    c = ImageChops.subtract_modulo(img1,img2)
    c.show()
    pass

with Image.open("animacion/mapa_prueba.bmp") as img:

    a = img.crop((0, 0, 8, 8))
    b= img.crop((0, 0, 8, 8))
    #b= img.crop((8, 0, 16, 8))
    arr = np.asarray(c)
    print(np.asarray(c))
    #img1 = img.transform((300, 300), Image.EXTENT, 
    #   data =[10, 0, 10 + img.width // 4, img.height // 3 ])
 # 
  #  img1.show()
    #a.save("t.bmp")
