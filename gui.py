import streamlit as st
from file_handling import *
from compression import *
from decompression import *


st.set_page_config(
    page_title="Vector Quantization",
    layout='wide'
)

st.title("Vector Quantization")
st.write("Lossy compression technique used to compress Grayscale images (LBG algorithm)")


option = st.radio("Choose an option:"
                  , ["Compression" , "Decompression"]
                  ,index=None)


if option == "Compression":

   uploaded_image = st.file_uploader("Choose an image file:"
                     , type= ["png", "jpg", "jpeg"])

   block_size = st.number_input("Enter the block size (if it's 2*2 enter 4):"
                                ,min_value=0)
   #min value used to prevent -ve and if min_value = 0 the cell accept only integers if 0.0 it accepts float numbers

   codebook_size = st.number_input("Enter the number of blocks in Codebook:"
                                   , min_value=0)


   if st.button("Encode Image"):

       image, old_mode = load_image(uploaded_image.name)
       image = check_padding(image, block_size)
       #  call encoding functions here :
       blocks = divide_image_into_blocks(image, block_size)
       initial_centroid = calculate_initial_centroid(blocks)


elif option == "Decompression" :

    compressed_image = st.file_uploader("Choose the file of Compressed/Binary Stream of Image:"
                                        , type=["txt", "bin"])
    codebook_file = st.file_uploader("Choose the file of the Codebook:"
                                     , type= ["txt", "bin"])


    if st.button("Decode Image"):
        # call decoding functions here
        i=0 # it has no meaning delete it after calling the decoding functions
