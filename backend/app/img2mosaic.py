from PIL import Image
from io import BytesIO
import base64
 
def convert(base64img, pixel_size, colors, inp="", output=""):
    if(inp):
        img = Image.open(inp)
    else:
        img = Image.open(BytesIO(base64.b64decode(base64img)))
 
    img = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        resample=Image.NEAREST
    )
 
    img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
    
    if(output):
        img.save(output)
    else: 
        img = img.convert('RGB')
        pixels = list(img.getdata())
        width, height = img.size
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
        return pixels

if __name__ == "__main__":
    inp = "D:/WebstormProjects/wugfsyefg/nosql2h23-mosaic/backend/app/a.jpg"
    #index = inp.find('base64,')
    #inp = inp[index+7:]
    output = "D:/WebstormProjects/wugfsyefg/nosql2h23-mosaic/backend/app/mosaic.png"
    pixel_size = 10
    colors = 2
    convert("", pixel_size, colors, inp, output)