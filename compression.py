import numpy as np

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
    initial_centroid = np.mean(blocks, axis=0)
    # print(initial_centroid) # debugging only
    return initial_centroid