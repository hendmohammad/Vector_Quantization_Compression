import struct  #used to write binary files
from PIL import Image #library to handle images
import numpy as np #this library used to treat th image as a vector of pixels' values and ease LBG calculations
from math import *
from compression import *


# The image must have dimensions that divided by block_size to can compress all pixels
# , so we solve this problem using padding
def check_padding(image , block_size): #if the image need padding implement it if not: do nothing
    width, height = image.size
    block_size = int(round(sqrt(block_size)))
    if height % block_size != 0 or width % block_size != 0:
        image = image_padding(image, block_size)

    return image

# padding logic :
def image_padding(image, block_size):
    old_width, old_height = image.size
    height_padding = (block_size - old_height % block_size) % block_size # calculate the number of pixels needed for height to be divided by block_size
    width_padding = (block_size - old_width % block_size) % block_size  # calculate the number of pixels needed for width to be divided by block_size
    image= np.array(image)
    padded_image_array  = np.pad(image, ((0 , height_padding), (0,width_padding)) , mode="edge") #datatype is nd.array
    # pad_width: ((padding to rows on  the top , padding rows on  the bottom) , (padding to columns on the left , padding to columns on the right))
    # based on that we can pad the image like this ((height_padding/2 , height_padding/2), (width_padding/2 , width_padding/2)),but this will lead to handle if the padding was odd
    # to round the values to (0 , value of padding) is easier and straightforward.

    padded_image = Image.fromarray(padded_image_array) #datatype is PIL.Image.Image

    return padded_image


def load_image(image_name):    #will be replaced after implementing the GUI
    #open image and check its mode and size
    image = Image.open("Input/"+image_name)
    # this algorithm only deals with gray scale images ,so if the image.mode != L (grayscale) convert it to grayscale
    old_mode = image.mode
    if image.mode != "L":
        image = image.convert('L')
    image= image.resize((512,512)) #for quick outputs , it will be deleted before submission as it has no effect on the logic
    return image , old_mode

def write_codebook(codebook , file_name):
    with open(file_name , "wb") as file:
        file.write(struct.pack("<HB" , len(codebook) , codebook[0].shape[0]))
        #codebook[0] means the first centroid  and shape[0] means the value of first dimension can be 1 also
        # it does not matter if it is the first centroid or not because they all have the same shape
        for centroid in codebook:
            pixel = np.round(centroid).astype(np.uint8) #uint8 is unsigned 8-bit integer :whole numbers from 0 : 255
            file.write(pixel.tobytes()) #convert each pixel to one byte (pixel value is in 0 : 255 )

def save_compressed_image(indices , codebook_size , original_size ,padded_size,old_mode , file_name):

    encoded_mode = old_mode.encode("ascii")
    bits_per_index = max(1, ceil(log2(codebook_size)))
    bits = ""
    for index in indices:
        bits += format( index , "0" + str(bits_per_index) + "b")

    while len(bits) % 8 != 0:
        bits += "0"

    data = bytearray()
    for i in range (0, len(bits), 8):
        data.append(int(bits[i:i+8], 2))

    with open(file_name , "wb") as file:
        file.write(struct.pack("<HHHHBB" , original_size[0] , original_size[1] , padded_size[0] , padded_size[1] , bits_per_index,len(encoded_mode)))
        # "<" => little endian the least significant byte is stored first
        # "H" unsigned integer in 2 byte , its number indicates the number of values
        # "B" unsigned integer in 1 byte
        file.write(encoded_mode)
        file.write(data)

    return bits # to write the binary stream in the gui , can be deleted as it does not affect the logic


#test write files and save them to use as input in decompression
#should be deleted before submission

block_size = 64
codebook_size = 16

image, old_mode = load_image("image1.jpg")
original_size = image.size             # before padding
image = check_padding(image, block_size)
padded_size = image.size               # after padding

codebook = gen_codebook(image, block_size, codebook_size)
indices = encoding(image, block_size, codebook)

write_codebook(codebook, "Output/codebook.bin")
data = save_compressed_image(indices, codebook_size, original_size, padded_size, old_mode,"Output/compressed.bin")
print(data)
