import streamlit as st
from file_handling import *
from compression import *
from decompression import *
import os


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
       image, old_mode = load_image(uploaded_image.name) #load image and if it is not grayscale convert it to grayscale
       padded_image = check_padding(image, block_size) #apply padding if needed

       #  call encoding functions here :
       codebook = gen_codebook(padded_image , block_size ,  codebook_size) #compression logic

       indices = encoding(image , block_size , codebook) # encoding the codebook => each block replaced by index
       write_codebook(codebook , "Output/codebook.bin")
       binary_stream = save_compressed_image(indices , codebook_size , image.size ,padded_image.size ,old_mode,"Output/compressed.bin")

       if os.path.exists("Output/compressed.bin"):
           st.success("Image compressed successfully") #random message to enhance the gui

           # write binary stream for quick overview
           st.write("Binary Stream: ", binary_stream)

           # save data for download buttons
           with open("Output/compressed.bin", "rb") as file:
               st.session_state["compressed_image"] = file.read()
           with open("Output/codebook.bin", "rb") as file:
               st.session_state["codebook"] = file.read()

       else:  #if any error in compression leads to not save the file
           st.error("Image compressed unsuccessfully")

   #clicking buttons in streamlit runs the script again ,so if download buttons  in (if st.button("Encode Image")) when we click on one of the two buttons the.
   if "compressed_image" in st.session_state and "codebook" in st.session_state:

       st.download_button("Download the Compressed Image", data=st.session_state["compressed_image"],file_name="compressed.bin")

       st.download_button("Download the Codebook", data=st.session_state["codebook"], file_name="codebook.bin")





elif option == "Decompression" :

    compressed_image = st.file_uploader("Choose the file of Compressed/Binary Stream of Image:"
                                        , type=["txt", "bin"])
    codebook_file = st.file_uploader("Choose the file of the Codebook:"
                                     , type= ["txt", "bin"])


    if st.button("Decode Image"):
        # call decoding functions here
        i=0 # it has no meaning delete it after calling the decoding functions
