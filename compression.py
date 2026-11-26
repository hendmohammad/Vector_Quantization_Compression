import numpy as np
import math

from numpy.ma.core import indices


def divide_image_into_blocks(image, block_size):
    # image into blocks
    image_array = np.array(image)  # image now is a 2D array (rows and columns)
    blocks = []
    height, width = image_array.shape  # image_array.shape returns a tuple first is the height and the second is the width
    block_size = int(round(math.sqrt(block_size))) # if the block_size not perfect square so we need to round it
    #without round : blocksize = 24 =>int(sqrt(blocksize)= 4 , but with round =>int(round(sqrt(blocksize))) = 5
    for row in range(0, height, block_size):  # iterate on the rows
        for col in range(0, width, block_size):  # iterate on the columns
            block = image_array[row: row + block_size, col: col + block_size]  # beginning : end
            # this means that we slice the image into small blocks  for example(2*2)
            blocks.append(block)  # append each block in the 3D list blocks
            # note that this line is in the second loop which means that the blocks stored horizontally means the shape will be(num of blocks , block size , block size)

    blocks = np.array(blocks)  # convert it to numpy array to ease calculations and be more clear if you want to print it
    # print(blocks) #debugging only
    return blocks


def calculate_initial_centroid(blocks):
    # calculating initial centroid

    # mean function here calculate the mean by adding each element and its corresponding in the next block and divide the sum by num of blocks
    initial_centroid = np.mean(blocks, axis=0)
    # print(initial_centroid) # debugging only
    return initial_centroid


def splitting(block):  # block is the centroid to split

    height, width = block.shape

    first_split = np.zeros((height, width))  # create first block of splitting with the same size of centroid 
    sec_split = np.zeros((height, width))  # create second block

    for i in range(0, height, 1):
        for j in range(0, width, 1):

            if block[i, j].is_integer():  # 10.0 >> integer
                first_split[i, j] = block[i, j] - 1
                sec_split[i, j] = block[i, j] + 1  # if int, add/subtract 1 from the original value

            else:  # 10.5 >> not integer
                first_split[i, j] = math.floor(block[i, j])
                sec_split[i, j] = math.ceil(block[i, j])

    return first_split, sec_split

def distance(block1, block2):
    diff = np.abs(block1 - block2)
    dis = np.sum(diff)
    return dis

def update_groups(codebook,blocks):  # blocks are all the vectors of the image, codebook is a list of all the splitted centroids to compare with (2 centroids in first step and inc.)

    distances = []
    for centroid in codebook:
        distance = np.abs(blocks - centroid).sum(axis=(1 , 2))
        distances.append(distance)

    distances = np.array(distances)
    nearest_centroid = np.argmin(distances , axis=0)

    new_codebook = []
    for i in range(len(codebook)):
        group = blocks[nearest_centroid==i]
        if len(group) > 0:
            new_centroid = np.mean(group, axis=0)
        else:
            new_centroid = codebook[i]

        new_codebook.append(new_centroid)

    return new_codebook


def gen_codebook(image, block_size, codebook_size):
    # 1) divide image into blocks
    blocks = divide_image_into_blocks(image, block_size)
    if codebook_size > len(blocks):
        raise ValueError('codebook_size can not be larger than number of blocks! Try smaller value.')

    # 2) calc initial centroid
    initial_centroid = calculate_initial_centroid(blocks)
    codebook = [initial_centroid]

    # 3) keep splitting until the required size is reached
    while len(codebook) < codebook_size:
        needed_codewords = codebook_size - len(codebook) #number of needed codewords
        new_codebook = []
        for i  in range(len(codebook)):
            if i < needed_codewords:  #split codewords (blocks) until reach the required number (codebook size)
                centroid1, centroid2 = splitting(codebook[i])  # split the centroid into two
                new_codebook.append(centroid1)
                new_codebook.append(centroid2)
            else:
                new_codebook.append(codebook[i])

        codebook = new_codebook

        # 4) keep updating until the centroids don't change
        for i in range(100): # for large numbers of codebook sizes 100 may be too large
            old_codebook = np.array(codebook)  # store the resulted centroids
            codebook = update_groups(codebook, blocks) # calculate nearest vector and average
           # print(f"codebook size{len(codebook)} , iteration {i}") # for debugging
            if np.allclose(old_codebook, np.array(codebook) , atol=0.05):  # func that checks whether two NumPy arrays have approx. equal values or not
                break

    return codebook

#encoding only find the distance between each block and the centroids in codebook
def encoding(image , block_size , codebook):
    blocks = divide_image_into_blocks(image, block_size)
    indices = []
    for block in blocks:
        distances = []
        for centroid in codebook:
            distances.append(distance(centroid, block))

        indices.append(int(np.argmin(distances)))

    return indices