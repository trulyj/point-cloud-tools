#Converts unlabeled point cloud scans scans into pickle files for use with PointNet++. Uses as input point cloud scans in .txt form.
#The locations of these files are indicated by paths.txt, which contains the paths to the directories where the files are stored.
#Additionally, saves rotated versions of the point cloud to the pickle file to augment the data.


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

def print_one_label (filename): #since these are unlabeled, this function always outputs 0s, but can be modified to output labels when they're available.
    return 0 

def print_one_line (points):
    split_line = points.split()
    a = np.array([100,100,100]);
    if split_line[0] == "nan" or split_line[1] == "nan" or split_line[2] == "nan":
        a = np.array([100,100,100]); #writes dummy, out of range, values to the array to be checked for and removed later
    else: 
        a = np.array([float(split_line[0]),float(split_line[1]),float(split_line[2])]); #converts line to numbers and enters them into the array
    return a


read = open(os.path.join(META_PATH, "paths.txt"), "r") #paths.txt contains paths to various directories containing point cloud files
dataArray = []#np.empty((12))
labelArray = []#np.empty((12))
index = 0
class_frq = np.zeros(11)
for line in read:  #for each file indicated by paths.txt
    directory = line.rstrip()
    file_dat = np.empty((0,3))
    file_dat_xy = np.empty((0,3))
    file_dat_yz = np.empty((0,3))
    file_dat_xz = np.empty((0,3))
    file_dat_yzx = np.empty((0,3))
    file_dat_zxy = np.empty((0,3))
    file_lab = np.empty((0))
    if len(os.listdir(directory)) == 0: #if directory is empty don't process it, just output "empty" to the screen.
        print("empty")
    else:
        print(directory)
        class_vec = np.zeros(11)
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
                        lab = print_one_filename(file)
                        if dat[0] != 100 or dat[1] != 100 or dat[2] != 100:
                            dat_xy = np.array([dat[1],dat[0],dat[2]]); #store rotations of the data by swapping coordinates.
                            dat_yz = np.array([dat[0],dat[2],dat[1]]);
                            dat_xz = np.array([dat[2],dat[1],dat[0]]);
                            dat_yzx = np.array([dat[1],dat[2],dat[0]]);
                            dat_zxy = np.array([dat[2],dat[0],dat[1]]);
                            
                            file_lab = np.concatenate((file_lab, [lab]), axis=0)
                            file_dat = np.concatenate((file_dat, [dat]), axis=0)
                            file_dat_xy = np.concatenate((file_dat, [dat_xy]), axis=0)
                            file_dat_yz = np.concatenate((file_dat, [dat_yz]), axis=0)
                            file_dat_xz = np.concatenate((file_dat, [dat_xz]), axis=0)
                            file_dat_yzx = np.concatenate((file_dat, [dat_yz]), axis=0)
                            file_dat_zxy = np.concatenate((file_dat, [dat_xz]), axis=0)

        labelArray.append(file_lab);
        dataArray.append(file_dat);
        labelArray.append(file_lab);
        dataArray.append(file_dat_xy);
        labelArray.append(file_lab);
        dataArray.append(file_dat_yz);
        labelArray.append(file_lab);
        dataArray.append(file_dat_xz);
        labelArray.append(file_lab);
        dataArray.append(file_dat_yzx);
        labelArray.append(file_lab);
        dataArray.append(file_dat_zxy);
        print(file_dat_zxy)
    print("read",directory)
    #print(labelArray)
    #print(dataArray)
    #print(np.shape(labelArray))
    #print(np.shape(dataArray))
    #print(labelArray[index])
    #print(dataArray[index])
    index = index+1

pickle.dump(labelArray, open("labels_aug.pickle", "wb")) #as the program crruently is, label array contains zeros since these pickle files are made for testing purposes, not training purposes.
pickle.dump(dataArray, open("data_aug.pickle", "wb"))

