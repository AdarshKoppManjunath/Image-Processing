
""" 
This program is written in python3 and can execute using visual studio code.
To execute this code, we need to have an input image in the raw format, and below command will help in running this program.

python "anugalrsector.py" "<input_imag_path>"  <inputimage_col> <inputimage_row> "<outputimage_path>"

anugalrsector.py : is the file name
input_image_path: input image file path 
output_image_path: directory path where output image can be saved
input_images_rows: rows of input image
input_image_cols: columns of input image"""





#required libraries
import numpy as np
import sys
import math
import cmath
from matplotlib import pyplot as plt


def read_image_into_array(file_name,input_cols,input_rows):
    """This function will take an image file in raw format and will convert it into ndarray

    Params:
        file_name(str): input image file path(.raw) 
        input_rows: image witdh, buffer needed to be for ndarray
        input_cols: image height, buffer needed to be for ndarray
    Return:
        input_image_array(ndarry): image converted into array"""

    input_image= open(file_name) #open image file
    input_image_array = np.fromfile(input_image, dtype = np.uint8, count = input_rows*input_cols) #image is read into array. 
    input_image_array.shape = (input_image_array.size//input_cols,input_cols) #1D to 2D array
    original_image = input_image_array #copy the read image into new variable


    print("\n \n original image \n",original_image)
    return original_image

def complex_image(original_image):
    """This function takes original image and convert it into complex numpy array
    Param:
        original_image(ndarray): original image in numpy array
    Return:
        compl_image(ndarray): #complex numpy array for the image numpy array"""

    rows,cols=original_image.shape
    compl_image=np.zeros((rows,cols),dtype=complex) #buffer for complex image

    for i in range(original_image.shape[0]):
        for j in range(original_image.shape[1]):
            compl_image[i][j]=pow(-1,i+j)*float(original_image[i][j]) #complex numpy array for the image numpy array


    print("\n \n complex image-\n",compl_image)
    return compl_image 


def reverse_bits(row_index,n):
  """This function is used to reverse the array indices
Param:
    row_index(int): row
    n(int):  int(math.log(float(rows), 2.0))

Return:
    i(int): reversed index"""
 
  i=0
  #Reverse the array indices.

  for k in range(n):
    i = i * 2 + row_index % 2
    row_index = row_index // 2
  return int(i)



def fft1d(tf,N,new_index):
  """This function is used to apply fft on 1d array
Param:
    tf(ndarray): row or col 1d ndarray
    N(int): row or col
    new_index(list): reversed indicies
Return:
    tf(ndarray):fft result"""
  w=complex()
  tf1=np.zeros(N)+0*1j

  #Rearrange array element
  for i in range(N):
    tf1[int(new_index[i])] = tf[i]

  n = int(math.log(N, 2))
  M = 1     #The initial length of subgroups
  j = int(N / 2) #The number of pairs of subgroups
  

  for i in range(n): #Successive merging for n levels
    for k in range(j): #Merge pairs at the current level

      i1 = k * 2 * M #the start of the first group
      i2 = (k * 2 + 1)*M #the start of the second group
      for itr in range(M):
        w=complex(math.cos(np.pi*itr / M), math.sin(-np.pi * itr / M))
        ta = tf1[i2 + itr] * w
        tf1[i2 + itr] = 0.5 * (tf1[i1 + itr] - ta)
        tf1[i1 + itr] = 0.5 * (tf1[i1 + itr] + ta)
    M = 2 * M #Double the subgroup length
    j = int(j / 2) #The number of groups is reduced by a half4

  for i in range(N):
    tf[i] = tf1[i]
  return tf



def fft2d(original_image,compl_image):
    """This function is used to apply fft on column and row
    Param:
        original_image(ndarray): original image
        compl_image(ndarray): original image in complex ndarry
    Return: 
        dft(ndarray): fft applied on both row and col, combined"""
    
    rows,cols=original_image.shape
    new_index=[0]*rows
    n = int(math.log(float(rows), 2.0)) 
    dft=np.zeros((rows,cols),dtype=complex)

    #Apply 2D FFT to C_img[][] and store the result in DFT[][]

    #pass-1 Apply 1D FFT to each col of compl_image[][]

    for i in range(cols):
        new_index[i] = reverse_bits(i,n)
    tft_c=np.zeros(rows)+0*1j
    for i in range(rows):
        for j in range(cols):
                tft_c[j] = compl_image[i][j]  #Copy the column I from compl_image[][] to tft_c[]
        tft_c=fft1d(tft_c, cols,new_index)    # Apply 1D FFT to fft[] and return the result in tft_c[];
        for j in range(cols):
            dft[i][j] = tft_c[j]    #Copy tft_c[] to the column j of dft[][];

    # Pass 2: Apply 1D FFT to each row of DFT[][]

    for i in range(rows):
        new_index[i]=reverse_bits(i,n)
    
    tft=np.zeros(rows)+0*1j
    for j in range(cols):
        for i in range(rows):
                tft[i] = dft[i][j]  #Copy row I from dft[][] to tft[];
        
        tft=fft1d(tft, rows,new_index)  #Apply 1D FFT to tft[] and return the result in tft[]
        for i in range(rows):
            dft[i][j] = tft[i]  #Copy tft[] to the row I of dft[]
    
    
    print("\n \n dft-\n",dft)
    return dft
   


def angle_map(ROWS=256, COLS=256):
    
    r = np.arange(ROWS)
    c = np.arange(COLS)
    
    #meshgrid is to create a rectangular grid out of an array of  rows and an array of cols.
    cols, rows = np.meshgrid(c, r)
    cols, rows = cols-COLS/2, rows-ROWS/2
    
    #to avoid infinity when rows=0
    rows += 0.0000000001
    cols += 0.0000000001

    #np.arctan is used to calculate inverse tangent
    img = np.arctan(cols/rows)
    
    img[int(ROWS/2):, :] += np.pi
    img -= img.min()
    img /= img.max()
    img *= 2*np.pi
    
    return img


def sector(K, n):
    
    # K -> number of sectors,
    #      dimension of the vector.
    # n -> refers to kth sector, 
    #      n=0,1,2,...,K-1.
    
    dth = 2*np.pi/K
    upr = (n+1)*dth
    lwr = n*dth
    img = angle_map()
    idx = (img < upr)*(img >= lwr)
    img[idx]  = 1
    img[~idx] = 0
    return img

def scan_through_angualr(dft):
    k=128 #dimension of the vector
    ah=[] #angular histogram
    for i in range(k):
        temp = (abs(dft)*sector(k,i)).sum() #stores summation of spectra values in the ith sector
        ah.append(temp)

    print("\n\n Angular histogram\n")
    print(ah)
    return ah



def frequency_histogram_to_txt(ah,destination_path):
    """This function saves ah to a txt file

    Params:
       dft(ndarray): dft ndarry of type complex"""

    destination_path=destination_path+"\\ah_car.txt"
   
    np.savetxt(destination_path, ah, newline="\n")  #save ah to a txt file

    #display the histogram
    plt.figure()
    x = np.arange(0,128) # x axis
    plt.bar(x,ah,color="black",align="center")
    plt.title('Frequency Histogram of Spectrum using angular sector')
    plt.show()
        
    return True


if __name__ == "__main__":    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python angularsector.py "<input_imag_path>"  <inputimage_col> <inputimage_row> "<outputimage_path>" """


    if len(sys.argv)<5:
        print("hi")
        print("command format should be ---- \n python angularsector.py inputimage_path  inputimage_col inputimage_row outputimage_path\n")
    else:
        print("here")
        original_image=read_image_into_array(sys.argv[1],int(sys.argv[2]),int(sys.argv[3])) 
        compl_image=complex_image(original_image)
        dft=fft2d(original_image,compl_image)
        ah=scan_through_angualr(dft)
        frequency_histogram_to_txt(ah,sys.argv[4])