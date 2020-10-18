"""This program is written in python3 and can execute using visual studio code.

Prerequisites are-
Input image path, destination folder, input image width and image column

Command to execute this program-
python "novel q3.py" "<input image path>" "destination image directory>" <rows> <colms>"""


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


def devide(histogram,l,h):
    """This funtion is  to find the split position, m, such that [l, m] is the range of the left part, [m+1, h] the right part, and the difference between the two parts’ sum is minimum
    
    Params:
        histogram(list): histogram
    Return:
        mid(int): midpoint, index where array is divded """

    #print(len(histogram),l,h)
    histogram=histogram[l:h+1] #new array
    #print(l,h)
    #print(hr)
    difference={} #to store all differences
    for i in range(len(histogram)):
      right=histogram[i+1:]
      left=histogram[:i+1]
      difference[i]=abs(sum(right)-sum(left)) 

    #print(diff)

    mid=min(difference, key=lambda k: difference[k]) #to find the indices with least difference

    return int(mid+l)

def build(histogram,l,h,l2,h2,t):
    """This function is part of novel devide and conqure authored by Dr. Xue Dong Yang
    Params:
        histogram(list): histogram
        l,h,l2,h2 (int): low, high, lown,and highn respectively
        t(list): result mapping table
    
    Result:
        t(list): result mapping table """

    if (l<h):
        m=devide(histogram,l,h)
        t[m]=int((h2+l2)/2)
        build(histogram,l,m,l2,t[m],t)
        build(histogram,m+1,h,t[m]+1,h2,t)

    return t

def fill_missing_value(t):
    """This funtion is to fill the missing value in t
    Params:
        t(list): result mapping table
    Return:
        t(list): result mapping table"""

    for i in range(len(t)):
      if t[i]==-1:
        t[i]=t[i-1] #filling missing value with the neighbour value
    return t

def save_array_to_image(cumulative_histogram,original_image,destination_path,input_rows,input_cols):
    """This function is to save ndarray into raw image
    Params
        cumulative_histogram(list): cdf
        original_image(ndarray): original image
        destination_path(str): directory to dump all gamma corrected images in raw format
        input_rows(int): image witdh, buffer needed to be for ndarray
        input_cols(int): image height, buffer needed to be for ndarray"""
     
    save_image = np.zeros([input_rows,input_cols]) #new ndarray buffer for resized image
    save_image=save_image.astype(int) 
    for i in range(input_rows):
        for j in range(input_cols):
            save_image[i][j] = cumulative_histogram[original_image[i][j]]
    
    destination_path=destination_path+"\\fig1_novel.raw" #file name to save as image
    save_image.astype("int8").tofile(destination_path) #saving image in the output file
    plt.imshow(save_image,'gray') #display the image 
    plt.show()




if __name__=='__main__':
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python novel q3.py inputimage_path outputimage_path inputimage_col inputimage_row"""
    
    print(sys.argv)

    if len(sys.argv)<5:
                print("command format should be ---- \n python  novel q3.py inputimage_path outputimage_path inputimage_col inputimage_row\n")
    else:
           
            img=read_image_into_array(sys.argv[1],int(sys.argv[3]),int(sys.argv[4]))      
            hist=caluclate_histogram([],img,int(sys.argv[3]),int(sys.argv[4]))   
            t=build(hist,0,len(hist)-1,0,len(hist)-1,[-1]*len(hist))
            t=fill_missing_value(t)
            print(t)
            save_array_to_image(t,img,sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
         