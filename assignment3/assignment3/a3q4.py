"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python a3q4.py "<original image path> <original image row> <original image columns> <destination path>"""


import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpig
import sys




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
    return original_image


def convolve(image, filter, weight):
    """This function helps in performing the convolution of image and filter
    Params:
        image(ndarray)- original image
        filter(ndarray)- filter
        weight(int)- wieght for the sharpening using laplacian operator
        
    Return:
        out(ndarray)-convolution of image and filter result"""
    
    # height and width of the image
    col = image.shape[0]
    row = image.shape[1]
    
    # height and width of the filter
    filter_col = filter.shape[0]
    filter_row = filter.shape[1]
    
    height = (filter_col - 1) // 2
    width = (filter_row - 1) // 2
    
    #output numpy matrix with height and width
    out = np.zeros((col,row))

    #iterate over all the pixel of image X
    for i in np.arange(height, col-height):
        for j in np.arange(width, row-width):

            sum = 0 # for accumulation of weighted terms

            #iterate over the filter
            for k in np.arange(-height, height+1):   
                for l in np.arange(-width, width+1):  

                    #get the corresponding value from image and filter                
                      sum +=  (image[i+k, j+l] * filter[height+k, width+l])

            sharpening=image[i,j]-(weight*sum)
            if sharpening > 255:
                sharpening = 255
            elif sharpening < 0:
                sharpening = 0
                  
            out[i,j] = sharpening
     
    return out

def display_and_save_images(image,destination_path):
    """This function will display the image and save ndarray into image
    Params:
        image(ndarray): original image marked with template matching
        destination path(str): path where image needs to be saved"""

    plt.subplot(111)
    plt.imshow(image,'gray') # display the matched image. 
    plt.title('result')
    plt.show()
    #print(image)
    image.astype("int8").tofile(destination_path) #save ndarray into image
    return True




if __name__ == '__main__':
    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python a3q4.py <original image path> <original image row> <original image columns> <destination path>"""
    
    print(sys.argv)

    if len(sys.argv)<5:
                print("command format should be ---- \n python   python a3q4.py <original image path> <original image row> <original image columns> <destination path>\n")
    else:
           image = read_image_into_array(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
           print("\n \nOriginal Image \n - %s \n\n original image shape-%s "%(image,image.shape))
           
           laplacian= np.array([[0,1,0],[1,-4,1],[0,1,0]]) # Laplacian Operator
           print("\n laplacian operator \n ")
           print(laplacian)
           
           weights=[1,2,4]
           print("\n\n weights considered -",weights)

           for i in weights:

                print("\n \n for weight- ",i)
                laplacian_result = convolve(image, laplacian,i) 

                print("\n \n laplacian after sharpening\n ",laplacian_result)
                display_and_save_images(laplacian_result,sys.argv[4]+"\\a3q4 w"+str(i)+".raw")


           

           