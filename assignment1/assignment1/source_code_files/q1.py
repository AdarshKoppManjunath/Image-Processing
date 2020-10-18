

""" 
This program is written in python3 and can execute using visual studio code.
To execute this code, we need to have an input image in the raw format, and below command will help in running this program.

python q1.py "input_imag_path" "output_image_path" inputimage_col inputimage_row outputimage_col outputimage_row

q1.py : is the file name
input_image_path: input image file path 
output_image_path: directory path where output image can be saved
input_images_rows: rows of input image
input_image_cols: columns of input image
outputimage_col: columns of output image
outputimage_row: rows of output image

"""
#import numpy library to create image array
import numpy as np
import sys
from matplotlib import pyplot as plt


def read_image_into_array(file_name,input_cols,input_rows,output_cols,output_rows):
    """This function will take an image file in raw format and will convert it into ndarray.

    Params:
        file_name(str): input image file path(.raw) 
        input_rows: image witdh, buffer needed to be for ndarray
        input_cols: image height, buffer needed to be for ndarray
    Return:
        input_image_array(ndarry): image converted into array"""

    input_image= open(file_name) #open image file
    input_image_array = np.fromfile(input_image, dtype = np.uint8, count = input_rows*input_cols) #image is read into array. 
    print(input_image_array)
    input_image_array.shape = (input_image_array.size//input_cols,input_cols) #1D to 2D array
    original_image = input_image_array #copy the read image into new variable
    resized_image = np.zeros([output_rows,output_cols]) #new ndarray buffer for resized image
    resized_image=resized_image.astype(int) #set ndarray elements to int type
    print(resized_image) 

    return original_image,resized_image


def resampling(old_image,resample_x,resample_y):
    """Source:  This funtion is for resampling authored by Dr. Xue Dong Yang

    Params:
        old_image(ndarray): original image in ndarray format
        resample_x, resample_y: resample positions
    Output:
        result:resampled intensity value at resample_x and resampl_y postions"""



   
    cols = int(resample_x)
    rows = int(resample_y)
    

    distance_x = (resample_x - cols)
    distance_y = (resample_y- rows)
    

    result = old_image[rows,cols]*(1.0-distance_x)*(1.0-distance_y)+old_image[rows,cols+1]*distance_x*(1.0-distance_y)+old_image[rows+1,cols]*(1.0-distance_x)*distance_y+old_image[rows+1,cols+1]*distance_x*distance_y
    return int(result)



def resize(old_image, new_image, input_cols, input_rows, output_cols, output_rows,destination_path):
    """Source:  This funtion is for resizing authored by Dr. Xue Dong Yang

      
    Params:
        old_image(ndarray): input image in ndarray format
        new_image(ndarray): out_put image buffer to write resized image
        input_cols(int): input image columns
        input_rows(int): input image rows
        output_cols(int): output image columns
        output_rows(int): output image rows
        destination_path(str): destination path where image needs to be saved."""


  
    resample_x = 0.0
    resample_y = 0.0

    #interval length

    Dx = float(input_cols- 1)/(output_cols - 1) 
    Dy = float(input_rows - 1)/(output_rows - 1)
    
   
    for row in range(output_rows):
        
        resample_y+= Dy
       
        for col in range(output_cols):
             
            if resample_x >=(input_cols-1) or resample_y>=(input_rows-1):
                #avoid accessing input image array when resample postions greater than input image rows and cols
                break
            new_image[row][col] = resampling(old_image, resample_x,resample_y)
            resample_x += Dx
        resample_x=0.0
        
    
    print(new_image.shape)
    new_image.astype("int8").tofile(destination_path) #saving image in the output file
    plt.imshow(new_image,'gray') #display the image 
    plt.show()

if __name__ == "__main__":    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python q1.py inputimage_path outputimage_path inputimage_col inputimage_row outputimage_col outputimage_row"""


    if len(sys.argv)<6:
        print("command format should be ---- \n python q1.py inputimage_path outputimage_path inputimage_col inputimage_row outputimage_col outputimage_row\n")
    else:
        old_image,new_image=read_image_into_array(sys.argv[1],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])) 
        resize(old_image,new_image,int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),sys.argv[2]) 