from PIL import Image #library to handle images
import numpy as np #this library used to treat th image as a vector of pixels' values and ease LGB calculations


def load_image(image_name):    #will be replaced after implementing the GUI
    #open image and check its mode and size
    image = Image.open("Input/"+image_name)
    # this algorithm only deals with gray scale images ,so if the image.mode != L (grayscale) convert it to grayscale
    old_mode = image.mode
    if image.mode != "L":
       image = image.convert("L")

    # The image must have equal dimensions(square) to divide it into  equal blocks
    # , so we can solve this problem using padding or resizing with the max dimension
    # and also save the old dimension

    old_height, old_width = image.size

    if old_height != old_width:  # if dimension not equal find the max and resize based on it
          new_dimension = max(old_width, old_height)
          image = image.resize((new_dimension, new_dimension))
    # if equal: do nothing
    return image , old_width, old_height, old_mode





