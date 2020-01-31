#Converts unlabeled point cloud scans scans into .npy files for use with PointNet. Uses as input point cloud scans in .txt form.
#The locations of these files are indicated by robo_paths.txt, which contains the paths to the directories where the files are stored.
#Outputs one .npy file for each input .txt file.

#All lines regarding labels are commented out since the data being converted was unlabeled, but can be uncommented and
#used if input data were to contain labels.

import glob
import os
import sys
import re
import shutil
import linecache
import pickle
import numpy as np
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #current directory
ROOT_DIR = os.path.dirname(BASE_DIR) #parent directory

META_PATH = BASE_DIR #os.path.join(BASE_DIR, 'meta')

def print_one_label (file): #since these are unlabeled, this function always outputs 0s, but can be modified to output labels when they're available.
    return 0 

def print_one_line (points):
    split_line = points.split()
    if split_line[0] == "nan" or split_line[1] == "nan" or split_line[2] == "nan":
        a = np.array([100,100,100,100,100,100]); #writes dummy, out of range, values to the array to be checked for and removed later
    else: 
        a = np.array([float(split_line[0]),float(split_line[1]),float(split_line[2]),0,0,0]); #converts line to numbers and enters them into the array
        #the three extra zeroes at the end signify RGB values and can be kept as 0s if the txt file has no color information, or can be changed to split_line[3], etc. if exporting from a file w/ RGB info
    return a

read = open(os.path.join(META_PATH, "paths.txt"), "r") #paths.txt contains paths to various directories containing point cloud files
dataArray = []
labelArray = []
index = 0
for line in read:  #for each file indicated by paths.txt
    directory = line.rstrip()
    file_dat = np.empty((0,6))
    #file_lab = np.empty((0))
    if len(os.listdir(directory)) == 0: #if directory is empty don't process it, just output "empty" to the screen.
        print("empty")
    else:
        print(directory)
        for file in os.listdir(directory):
            print(file)
            if os.path.getsize(os.path.join(directory, file)) > 0: #if file isn't empty, process it.
                readfile = open(os.path.join(directory, file), "r")
                print("file read")
                counter = 0
                for l in readfile:
                    counter = counter + 1
                    if counter > 12: #ignore first 12 lines of file. Can be commented out or modified for files with no filler lines.
                        dat = print_one_line(l)
                        lab = print_one_label(file)
                        if dat[0] != 100 or dat[1] != 100 or dat[2] != 100:
                            class_vec[lab] = 1 
                            #file_lab = np.concatenate((file_lab, [lab]), axis=0)
                            file_dat = np.concatenate((file_dat, [dat]), axis=0)
        fname = "pc" + str(index) + ".npy" 
        np.save(fname, file_dat) #append each file's data to the full dataArray
        #np.save(fname, file_lab)
        print("read",directory)
        index = index+1

