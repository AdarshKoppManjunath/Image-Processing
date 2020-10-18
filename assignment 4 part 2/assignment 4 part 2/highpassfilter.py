
""" 
This program is written in python3 and can execute using visual studio code.
To execute this code, we need to have an input image in the raw format, and below command will help in running this program.

python highpassfilter.py "<input_imag_path>"  <inputimage_col> <inputimage_row> "<outputimage_path>"

highpassfilter.py : is the file name
input_image_path: input image file path 
output_image_path: directory path where output image can be saved
input_images_rows: rows of input image
input_image_cols: columns of input image


"""
#required libraries
import numpy as np
import sys
import math
import cmath
from matplotlib import pyplot as plt


def read_image_into_array(file_name,input_cols,input_rows):
    """This function will take an image file in raw format and will convert it into ndarray.

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



def fft2d(compl_image):
    """This function is used to apply fft on column and row
    Param:
        original_image(ndarray): original image
        compl_image(ndarray): original image in complex ndarry
    Return: 
        dft(ndarray): fft applied on both row and col, combined"""
    
    rows,cols=compl_image.shape
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
    
    
    #print("\n \n dft-\n",dft)
    return dft

def distance(pos1,pos2):
    #distance between point2 ( center) and point 2 ( j,i)
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

def ideal_high_pass_filter(D0,img_shape):
    f = np.ones(img_shape[:2]) #initialize base with zeros (filter)
    rows, cols = img_shape[:2] #image size
    center = (rows/2,cols/2)  #center poistion
     #distance to the center is caluclated for all the points. If its less than cut off then set it  to 0
    for i in range(cols):
        for j in range(rows):
            #if distance is less than cutoff 
            if distance((j,i),center) < D0:
                f[j,i] = 0
    return f


def ifft2d(highpassfiltered_image):
    """This function is used to apply inverse fft 
    Param:
        lowpassfiltered_image(ndarray): fft*hf
    Return: 
        idft(ndarray): inverse fft"""
    
    rows,cols=highpassfiltered_image.shape

    idft=np.zeros((rows,cols),dtype=complex)

   # we are conjugating the fft*hf and applying fft2d on that 
    for i in range(rows):
        for j in range(cols):
            highpassfiltered_image[i][j]=np.conjugate(highpassfiltered_image[i][j])
    
    idft=fft2d(highpassfiltered_image)
   
    idft=idft*rows*rows

    return idft


def caluclate_magnitude(idft):
    """This function is used to compute magnitude of idft
    Param:
        idft(ndarray): ifft applied on both row and col, combined
    Return:
        mag(ndarray): magnitude values float ndarray
        """

    #Compute the magnitude of dft[][]
    rows,cols=idft.shape
    mag_idft=np.zeros((rows,cols),dtype=int)
   
    for i in range(rows):
            for j in range(cols):
                mag_idft[i][j] = abs(idft[i][j])  #caluclates the magnitude of a complex number same as math.sqrt(idft[i][j].real * idft[i][j].real +idft[i][j].imag * idft[i][j].imag
               

    print("\n \n magnitude-\n",mag_idft)
    return mag_idft

def display_and_save_images(mag_idft,destination_path):
    """This function will display the image and save ndarray into image
    Params:
        mag_idft(ndarray): magnitude of id
        destination path(str): path where image needs to be saved"""
    

    plt.subplot(111)
    plt.imshow(mag_idft,'gray') # display the image. 
    plt.title('result')
    plt.show()
    #print(image)
    destination_path=destination_path+"\\hf_sqr_cutoff_60.raw"
    mag_idft.astype("int8").tofile(destination_path) #save ndarray into image
    return True


if __name__ == "__main__":    
    """Command line arguments will be recived here. Input or command to run this program should be in the below format 
    python highpassfilter.py "<input_imag_path>"  <inputimage_col> <inputimage_row> "<outputimage_path>" """


    if len(sys.argv)<5:
        
        print("command format should be ---- \n python highpassfilter.py inputimage_path  inputimage_col inputimage_row outputimage_path\n")
    else:
         #image to ndarray
        original_image=read_image_into_array(sys.argv[1],int(sys.argv[2]),int(sys.argv[3])) 

        #ndarray image to complex
        compl_image=complex_image(original_image)

        #apply fft2d
        dft=fft2d(compl_image)
        print("\n dft\n ", dft)

        #high pass filter
        D0=10
        hf= ideal_high_pass_filter(D0,[256,256])
       
        #display high pass filter
        plt.subplot(111)
        plt.imshow(abs(hf), "gray")
        plt.title("Ideal High Pass")
        plt.show()

        #apply high pass filter on caluclated fft
        print("\n\n High pass filter with the cut off frequency - 60 \n \n", hf)
        highPassCenter = dft * hf
        print("\n\n fft * hf \n \n", highPassCenter)

        #apply inverse fft on highpasscenter
        idft=ifft2d(highPassCenter)
        print("\nidft \n",idft)
        
        #caluclate the magnitude of idft
        mag_idft=caluclate_magnitude(idft)

        #display and save 
        display_and_save_images(mag_idft/256,sys.argv[4])
        