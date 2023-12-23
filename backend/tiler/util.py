import tiler as tl
import cv2
import base64

def tiler(img_string):
    #with open("test.png", "rb") as image_file:
    #    img_string = base64.b64encode(image_file.read())
    img = tl.tile_img(img_string)
    #cv2.imwrite('out.png', img)
    retval, buffer = cv2.imencode('.png', img)
    string_img = base64.b64encode(buffer)
    return string_img

