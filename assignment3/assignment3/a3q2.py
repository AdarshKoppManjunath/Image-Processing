"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python a3q2.py "<original image path> <original image row> <original image columns> <destination path>"""




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


def convolve(image, filter):
    """This function helps in performing the convolution of image and filter
    Params:
        image(ndarray)- original image
        filter(ndarray)- filter
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
                  
            out[i,j] = sum 
     
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
    return True #returing for the continuation- dummy

if __name__ == '__main__':
    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python  a3q2.py "<original image path> <original image row> <original image columns> <destination path>"""
    
    print(sys.argv)

    if len(sys.argv)<5:
                print("command format should be ---- \n python a3q2.py <original image path> <original image row> <original image columns> <destination path>\n")
    else:
           image = read_image_into_array(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
           print("\n \nOriginal Image \n - %s \n\n original image shape-%s "%(image,image.shape))

           gradient_x = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]) # Sobel (Gradient) operator- 𝐺𝑥(𝑥, 𝑦) 
           gradient_y = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]]) # Sobel (Gradient) operator- 𝐺y(𝑥, 𝑦) 
           print("\n\n\n gradient-x \n %s \n\n \ngradient-y\n %s\n\n"%(gradient_x,gradient_y))

           gradient_x_out = convolve(image, gradient_x) 
           gradient_x_out = np.absolute( gradient_x_out) #negative values are abosluted- converted in the range of 0 - 255
           gradient_x_out=gradient_x_out.astype(int)
           print("\n\n\n gradient_x_out\n",gradient_x_out )

           display_and_save_images(gradient_x_out,sys.argv[4]+"\\gx.raw") #display and save gx

           gradient_y_out = convolve(image, gradient_y) 
           gradient_y_out = np.absolute(gradient_y_out)  #negative values are abosluted- converted in the range of 0 - 255
           gradient_y_out=gradient_y_out.astype(int)
           print("\n\n\n gradient_y_out\n",gradient_y_out)

   
           display_and_save_images(gradient_y_out,sys.argv[4]+"\\gy.raw") #display and save gy
           
           gradient = np.sqrt(np.power( gradient_x_out, 2) + np.power(gradient_y_out, 2))   #the gradient
           gradient = gradient.astype(int)
           print("\n\n\n gradient\n",gradient)

           display_and_save_images(gradient,sys.argv[4]+"\\g.raw")
          


            #the edge map with threshold TE = 128
           for i in range(gradient.shape[0]):
               for j in range(gradient.shape[1]):
                    if gradient[i][j]>=128:
                       gradient[i][j]=255
                    else:
                        gradient[i][j]=0

                    
           
           print("\n\n\n the edge map with threshold TE = 128\n",gradient)
           display_and_save_images(gradient,sys.argv[4]+"\\gedgemap128.raw")
           

            #output images