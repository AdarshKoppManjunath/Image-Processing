"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python a2q1.py "<input image path>" "destination image directory>" <rows> <colms>"""



import cv2 
import sys
import numpy as np 
from matplotlib import pyplot as plt




def read_image_into_array(file_name,input_rows,input_cols):
    """This function will take an image file in raw format and will convert it into ndarray.

    Params:
            file_name(str): input image file path(.raw) 
            input_rows(int): image witdh, buffer needed to be for ndarray
            input_cols(int): image height, buffer needed to be for ndarray
    Return:
            input_image_array(ndarry): image converted into array
            gamma_buffer(ndarray: buffer for gamma converted image"""

    input_image= open(file_name) 
    input_image_array = np.fromfile(input_image, dtype = np.uint8, count = input_rows*input_cols) #image is read into array. 
    #print(input_image_array)
    input_image_array.shape = (input_image_array.size//input_cols,input_cols) #1D to 2D array
    original_image=input_image_array
    gamma_buffer = np.zeros([input_rows,input_cols]) 
    gamma_buffer=gamma_buffer.astype(int) #set ndarray elements to int type
    return original_image,gamma_buffer


def powerlaw_transformation(image,gamma_corrected,gamma,input_rows,input_cols):

    """ This function is for power law transformation.
    Params:
        image(ndarray): input image in ndarray
        gamma_corrected(ndarray): buffer to copy gamma corrected image
        gamma(float): gamma value for gamma correction
        input_rows(int): image witdh, buffer needed to be for ndarray
        input_cols(int): image height, buffer needed to be for ndarray
    Return:
        gamma_corrected(ndarray): gamma corrected ndarray"""
    
    gamma_corrected = np.array(255*(image / 255  ) ** gamma, dtype = 'uint8') #gamma correction done here for the entire image ndarray and loaded it to gamma_corrected ndarray
    print(gamma_corrected.dtype)

    return gamma_corrected #return the gamma corrected ndarray

def save_array_to_image(gamma_corrected_array,gamma,destination_path):
    """This function is to save ndarray into raw image
    Params
        gamma_corrected_array(ndarray): gamma corrected ndarray
        gamm(float): gamma value to name the image file
        destination_path(str): directory to dump all gamma corrected images in raw format"""

    destination_path=destination_path+"\gamma corrected_fig2_"+str(gamma)+".raw" #name the image file with gamma
    gamma_corrected_array.astype("int8").tofile(destination_path) #saving image in the output file
    plt.imshow(gamma_corrected_array,'gray') #display the image 
    plt.show()
		

 
if __name__=='__main__':
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python a2q1.py inputimage_path outputimage_path inputimage_col inputimage_row"""
    
    print(sys.argv)

    if len(sys.argv)<5:
                print("command format should be ---- \n python  a2q1.py inputimage_path outputimage_path inputimage_col inputimage_row\n")
    else:
            img,gamma_buffer=read_image_into_array(sys.argv[1],int(sys.argv[3]),int(sys.argv[4]))
            for gamma in [0.3,1.0,1.8]: 
                gamma_corrected_array=powerlaw_transformation(img,gamma_buffer,gamma,sys.argv[3],sys.argv[4])
                save_array_to_image(gamma_corrected_array,gamma,sys.argv[2])

