import numpy as np
import math

def divide_image_into_blocks(image , block_size):
   #image into blocks
   image_array = np.array(image) #image now is a 2D array (rows and columns)
   blocks = []
   height , width = image_array.shape #image_array.shape returns a tuple first is the height and the second is the width
   # actually their order do not matter as the image has an equal dimensions
   for row in range(0 ,height , block_size ): # iterate on the rows
       for col in range(0 ,width , block_size): #iterate on the columns
            block = image_array[row : row+block_size , col : col+ block_size] # beginning : end
            #this means that we slice the image into small blocks  for example(2*2)
            blocks.append(block) # append each block in the 3D list blocks
            # note that this line is in the second loop which means that the blocks stored horizontally means the shape will be(num of blocks , block size , block size)

   blocks = np.array(blocks) #convert it to numpy array to ease calculations and be more clear if you want to print it
   #print(blocks) #debugging only
   return blocks


def calculate_initial_centroid(blocks):
    # calculating initial centroid

    # mean function here calculate the mean by adding each element and its corresponding in the next block and divide the sum by num of blocks
    avg = np.mean(blocks, axis=0) 
    initial_centroid = np.round(avg, 1) # to restrict it to one decimal digit
    # print(initial_centroid) # debugging only
    return initial_centroid


def splitting(block): # block is the centroid to split

    height , width = block.shape

    first_split = np.zeros((height, width))  # create first block of splitting with the same size of centroid 
    sec_split = np.zeros((height, width))    # create second block

    for i in range(0 ,height , 1 ): 
        for j in range(0 ,width , 1):

            if block[i,j].is_integer():              #  10.0 >> integer
                first_split[i, j] = block[i, j] - 1
                sec_split[i, j] = block[i, j] + 1    # if int, add/subtract 1 from the original value

            else:                                    # 10.5 >> not integer
                first_split[i, j] = math.floor(block[i, j]) 
                sec_split[i, j] = math.ceil(block[i, j])

    return first_split, sec_split


def updateGroups(codebook, blocks): # blocks are all the vectors of the image, codebook is a list of all the splitted centroids to compare with (2 centroids in first step and inc.)

    groups = [[] for i in range(len(codebook))] # e.g. create 4 empty groups for 4 centroids

    for b in blocks: # calc the distance of each vector with each centroid
        distances = []

        for centroid in codebook:
            distances.append(distance(centroid, b))

        shortest_index = np.argmin(distances) # get the index of the smallest distance in the list
        groups[shortest_index].append(b)

        # e.g. it will look like this
        # groups = [
        #    [B1, B3],   Closest to centroid1
        #    [B4],       Closest to centroid2
        #    [B2, B5],   Closest to centroid3
        #    [B6]        Closest to centroid4
        #]

    new_codebook = []
    for i in range(len(groups)):

        if len(groups[i]) > 0:
            avg = np.mean(groups[i], axis=0) 
            new_centroid = np.round(avg, 1) # to restrict it to one decimal digit
        else:
            new_centroid = codebook[i]

        new_codebook.append(new_centroid)

    return new_codebook


def distance(block1, block2):

    diff = np.abs(block1 - block2)
    height, width = diff.shape
    distance = 0

    for i in range(0 ,height , 1 ): 
        for j in range(0 ,width , 1):
            distance += diff[i, j]

    return distance


def genCodeBook(image, block_size, codebook_size):

    # 1) divide image into blocks & 2) calc initial centroid 
    blocks = divide_image_into_blocks(image, block_size)
    initial_centroid = calculate_initial_centroid(blocks)

    codebook = [initial_centroid]

    # 3) keep splitting until the required size is reached
    while len(codebook) < codebook_size:

        new_codebook = []

        for centroid in codebook:

            centroid1, centroid2 = splitting(centroid) # split the centroid into two
                
            new_codebook.append(centroid1)
            new_codebook.append(centroid2)

        codebook = new_codebook

        # 4) keep updating until the centroids don't change
        while True:
            old_codebook = np.array(codebook) # store the resulted centroids

            codebook = updateGroups(codebook, blocks) #

            if np.array_equal(old_codebook, np.array(codebook)): # func that checks whether two NumPy arrays have approx. equal values or not
                break

    return codebook
