"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python a3q1.py "<original image path> <original image row> <original image columns> <template image> <template image rows> <template image column> <destination path>"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
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



def get_correlation_matrix(image,template):
    """This function is to find correlation value between original and template image. Here we scan the template image over original image by taking a portion of original image
    which is of same size as template image
    
    Params: 
        image(ndarray): original image ndarray
        template(ndarray): template image ndarray

    Return:
        correlation(ndarry): ndarray which gives correlation between template and original image
    """
    
    col, row = image.shape #original image
    temp_col, temp_row= template.shape #template image

    # Set image, target and result value matrix
    image = np.array(image, dtype="int")     #setting ndarray elements to int
    template = np.array(template, dtype="int")  #setting ndarray elements to int
    correlation_values = np.zeros((col,row))
    

    #scanning original image with the template image for correlation
    for i in range(0, col-temp_col):
        for j in range(0, row-temp_row):
            
            #compare by clipping the original image which is of same width and height as template image

            original_image_part = image[i : i+temp_col, j : j+temp_row]
            correlation = np.sum(original_image_part * template)  #correlation - np.sum will multiply both template and portion selected and sum the result.
            normalize= np.sqrt( (np.sum(original_image_part ** 2))) * np.sqrt(np.sum(template ** 2)) #normalization factor 
            correlation_values[i,j] = (correlation/normalize)  #adding correlation value to the matrix

    return correlation_values

def match_template_on_original_image(image,template,correlation):
    """This function is used collect the pixel with highest correlation recorded i.e 0.99 or 1.0 and mark this matching on original image using square boxes
    Params: 
        image(ndarray): original image ndarray
        template(ndarray): template image ndarray
        correlation(ndarry): ndarray which gives correlation between template and original image

    Return:
        image(ndarray): original image ndarray, but its marked with the template matching using square boxes
    """
    
    
    #scan through correlation matrix.
    for i in range(correlation.shape[0]): 
      for j in range(correlation.shape[1]):
            
              #correlation values ranges from 0 to 1. If the value is 0.99 or more, we are considering it as match.
              if correlation[i][j]>=0.99:
                 match=(j,i)
                 print("\n template matched postion -%s    with the correlation-%s" %(match,correlation[i][j]))
                 cv2.rectangle(image,match,(match[0] + template.shape[1], match[1] + template.shape[0]), 0, 1) #writing a rectangle boundary for matching on the original image.
    return image


def display_and_save_the_matched_image(image,destination_path):
    """This function will display the image and save ndarray into image
    Params:
        image(ndarray): original image marked with template matching
        destination path(str): path where image needs to be saved"""

    plt.subplot(111)
    plt.imshow(image,'gray') # display the matched image. 
    plt.title('result')
    plt.show()
    print(image)
    destination_path=destination_path+"\\a3q1.raw"
    image.astype("int8").tofile(destination_path) #save ndarray into image
    


if __name__ == '__main__':
    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python a3q1.py "<original image path> <original image row> <original image columns> <template image> <template image rows> <template image column> <destination path>"""
    
    print(sys.argv)

    if len(sys.argv)<8:
                print("command format should be ---- \n python a3q1.py <original image path> <original image row> <original image columns> <template image> <template image rows> <template image column> <destination path>\n")
    else:
           image = read_image_into_array(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]))
           print("\n \n \n Original Image \n  %s \n\n original image shape-%s "%(image,image.shape))


           template = read_image_into_array(sys.argv[4],int(sys.argv[5]),int(sys.argv[6]))
           print("\n \n \n Template Image \n %s \n\n template image shape-%s "%(image,image.shape))

           correlation = get_correlation_matrix(image, template)
           print("\n \n \ncorrelation matrx \n ",correlation)

           image = match_template_on_original_image(image, template, correlation)
           display_and_save_the_matched_image(image,sys.argv[7])