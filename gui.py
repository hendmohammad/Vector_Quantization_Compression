#initial implementation
#will be replaced by the GUI
from file_handling import *
from compression import *
image_name = input("Please enter the name of the image: ")
block_size = int(input("Please enter the block size of the image(if (2*2) enter 4 and so on): "))
num_of_codeWords = int(input("Please enter the size of the codebook: "))
image , old_width , old_height , old_mode = load_image(image_name)
blocks = divide_image_into_blocks(image, block_size)
print("the blocks after dividing:")
print(blocks)
initial_centroid = calculate_initial_centroid(blocks)
print("initial centroid:")
print(initial_centroid)
