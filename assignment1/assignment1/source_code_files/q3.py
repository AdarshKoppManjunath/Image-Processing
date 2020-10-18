
""" 
This program is written in python3 and can execute using visual studio code.
To execute this code, we need to have an input image in the raw format, and below command will help in running this program.

python q3.py "input_imag_path" "output_image_path" input_images_rows input_image_cols pixel_level_in_list

q3.py : is the file name
input_image_path: input image file path 
output_image_path: directory path where output image can be saved
input_images_rows: rows of input image
input_image_cols: columns of input image
pixel_level_in_list: bits needs to be altered 


lets say if intensity quantization level is 128, then the command will be 
python q3.py "input-image-path" "destination-path" rows cols 7

if intensity quantization level=64  then pixel_level_in_list will be 76. Similary for all quantization levels. 


"""


#import numpy library to create image array
import numpy as np
#import sys to pass command line arguments
import sys
#matplotlib is to display images
from matplotlib import pyplot as plt



def read_image_into_array(file_name,input_rows,input_cols):
    """This function will take an image file in raw format and will convert it into ndarray.

    
    Params:
        file_name(str): input image file path(.raw) 
        input_rows: image witdh
        input_cols: image height
    Return:
        input_image_array(ndarry): image converted into ndarray"""

    input_image= open(file_name) #open image file
    input_image_array = np.fromfile(input_image, dtype = np.uint8, count = input_rows*input_cols) #image is read into ndarray. 
    print(input_image_array)
    return input_image_array #return image array

def convert_decimal_to_binary_array(input_image_index):
    """This function is to convert ndarry from decimal to binary format.
    
    Params:
        input_image_array(int): ndarray index which is decimal
    Return:
        output_image(ndarray): ndarray index which is binary"""
    if input_image_index==0: return ''
    else:
        return convert_decimal_to_binary_array(input_image_index//2) + str(input_image_index%2) # convert decimal to binary

def outputimage(input_image_array):
    """This function creates buffer for output image and convert input ndarray to binary and save it in output buffer

    Params:
        input_image_array(ndarray): input image ndarry in decimal
    return:
        output_image(ndarray): input image ndarray in binary"""

    output_image=np.array([]) #create ouput image buffer
    for index in input_image_array:
        binary=convert_decimal_to_binary_array(index) #convert all ndarray elements into binary format
        binary=(8-len(binary))*'0'+binary if len(binary) < 8 else binary  #check all elments are in 8 bits binary format
        output_image=np.append(output_image,binary)
    return output_image

def change_pixel(output_image,bits_needs_to_be_changed):
    """This function is to change the required bit for quantization level adjustment.
    Params:
        output_image(ndarray): ouput image in binary format
        bits_needs_to_be_changed(list): list of bits need to be reversed.
    Return:
        output_image(ndarry): bits modified accoriding to the required quantization level."""

    for index in range(len(output_image)):
        temperoray=list(output_image[index])
        for bit in list(bits_needs_to_be_changed):
            temperoray[int(bit)]='0'                     #take all bits need to be rest and set it to 0
        output_image[index]=''.join(temperoray)
    
    print(output_image)
    return output_image

def convert_binary_to_decimal(output_image):
    """ This function is to convert binary back to decimal ndarray.

    Params: 
        output_image(ndarray): ndarray with changed bits 
    Return:
        output_image(ndarray): ndarray in decimal"""

    for index in range(len(output_image)):
        output_image[index]=int("".join(str(x) for x in output_image[index]), 2)  #converting binary back to decimal
    output_image.shape=(output_image.size//256,256) #reshaping 1D to 2D
    output_image=output_image.astype(int)
    print(output_image)
    return output_image

def write_array_to_image(output_image,destination_path):
    """This function write back the ndarray to image
    Params:
        output_image(ndarry): ndarray in decimal with changed bits
    Return:
        destnation_path(str): changed ndarray is saved as new raw image"""

    print("write array to image\n")
    output_image.astype("int8").tofile(destination_path) #save ndarray into image
    plt.imshow(output_image,'gray')
    plt.show()

if __name__ == "__main__":    

    if len(sys.argv)<6:
        print("command format should be ---- \n python q3.py input_imag_path output_image_path input_images_rows input_image_cols pixel_level_in_list\n")
    else:
        input_image_array=read_image_into_array(sys.argv[1],int(sys.argv[3]),int(sys.argv[4]))
        output_image=outputimage(input_image_array)
        output_image=change_pixel(output_image,sys.argv[5])
        output_image=convert_binary_to_decimal(output_image)
        write_array_to_image(output_image,sys.argv[2])           
        
    
    

    



