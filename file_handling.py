from PIL import Image #library to handle images
import numpy as np #this library used to treat th image as a vector of pixels' values and ease LBG calculations


# The image must have dimensions that divided by block_size to can compress all pixels
# , so we solve this problem using padding
def check_padding(image , block_size): #if the image need padding implement it if not: do nothing
    height, width = image.size
    if height % block_size != 0 | width % block_size != 0:
        image = image_padding(image, block_size)

    return image


def image_padding(image, block_size):
    old_width, old_height = image.size

    height_padding = (block_size - old_height % block_size) % block_size
    width_padding = (block_size - old_width % block_size) % block_size

    padded_image_array  = np.pad(image, ((0 , height_padding), (0,width_padding)) , mode="edge") #datatype is nd.array
    padded_image = Image.fromarray(padded_image_array) #datatype is PIL.Image.Image

    return padded_image


def load_image(image_name):    #will be replaced after implementing the GUI
    #open image and check its mode and size
    image = Image.open("Input/"+image_name)
    # this algorithm only deals with gray scale images ,so if the image.mode != L (grayscale) convert it to grayscale
    old_mode = image.mode
    if image.mode != "L":
        image = image.convert('L')

    return image , old_mode

