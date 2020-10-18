"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python a2q2.py "<input image path>" "destination image directory>" <rows> <colms>"""


import numpy as np
from matplotlib import pyplot as plt
import sys


def read_image_into_array(file_name,input_rows,input_cols):
    """This function will take an image file in raw format and will convert it into ndarray.

    Params:
            file_name(str): input image file path(.raw) 
            input_rows(int): image witdh, buffer needed to be for ndarray
            input_cols(int): image height, buffer needed to be for ndarray
    Return:
            input_image_array(ndarry): image converted into array
            """
    input_image= open(file_name) 
    input_image_array = np.fromfile(input_image, dtype = np.uint8, count = input_rows*input_cols) #image is read into array. 
    #print(input_image_array)
    input_image_array.shape = (input_image_array.size//input_cols,input_cols) #1D to 2D array
    original_image=input_image_array
    return original_image

def caluclate_histogram(histogram,original_image,input_rows,input_cols):
    """This function is to caluclate histogram
    Params:
        histogram(list):empty list to fill histogram
        original_image(ndarray):original image
        input_rows(int): image width
        input_cols(int): image column
    Return:
        histogram(list): histogram"""

    

    for i in range(256):
        histogram.append(0)

    for i in range(input_rows):
        for j in range(input_cols):
            histogram[original_image[i][j]]+=1


    print(histogram)
    return histogram

def caluclate_cumulative_histogram(cumulative_histogram,histogram):
    """This function is to caluclate cumulative histogram
    Params:
        cumulative_histogram(list): empty list to fill cumlutaive histogram values
        histogram(list): histogram
    Return:
        cumulative_histogram(list): cumultaive histogram """

    q=0
    for i in histogram:
        q = q + i
        cumulative_histogram.append(q)
    print(cumulative_histogram)

    return cumulative_histogram

def plotting(array,destination_path):
    """This function is to plot histogram or cdf
    params:
        array(list): Histogram or cdf
        destination_path(str): path to save plot"""
    
    x = np.arange(0,256) # x axis
    plt.bar(x,array,color="black",align="center") #plot
    destination_path=destination_path+".png" #path to save
    plt.savefig(destination_path) #save
    plt.show()


def save_array_to_image(array,original_image,destination_path,input_rows,input_cols):
    """This function is to save ndarray into raw image
    Params
        array(list): histogram or cdf
        original_image(ndarray): original image
        destination_path(str): directory to dump all gamma corrected images in raw format
        input_rows(int): image witdh, buffer needed to be for ndarray
        input_cols(int): image height, buffer needed to be for ndarray"""
     
    save_image = np.zeros([input_rows,input_cols]) #new ndarray buffer for resized image
    save_image=save_image.astype(int) 
    for i in range(input_rows):
        for j in range(input_cols):
            save_image[i][j] = array[original_image[i][j]]
    
    destination_path=destination_path+".raw" #name the image file with gamma
    save_image.astype("int8").tofile(destination_path) #saving image in the output file
    plt.imshow(save_image,'gray') #display the image 
    plt.show()
		


if __name__=='__main__':
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python a2q1.py inputimage_path outputimage_path inputimage_col inputimage_row"""
    
    print(sys.argv)

    if len(sys.argv)<5:
                print("command format should be ---- \n python  a2q2.py inputimage_path outputimage_path inputimage_col inputimage_row\n")
    else:
            img=read_image_into_array(sys.argv[1],int(sys.argv[3]),int(sys.argv[4]))
            histogram=caluclate_histogram([],img,int(sys.argv[3]),int(sys.argv[4]))
            cdf=caluclate_cumulative_histogram([],histogram)
            plotting(histogram,sys.argv[2])
            plotting(cdf,sys.argv[2])
            save_array_to_image(histogram,img,sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
            save_array_to_image(cdf,img,sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
