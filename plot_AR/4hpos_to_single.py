# coding=utf-8
# !/usr/bin/env python
"""
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/12/14
"""
import os
from tkinter import filedialog
import numpy as np
import csv
import math

def readPOS(PosFile):
    converge_time = np.zeros([4], dtype=np.float32)
    f = open(PosFile, 'r')
    line = f.readlines()
    num = len(line)
    epoch = np.arange(0, num).reshape((num, 1))
    pos = np.zeros([num, 15], dtype=np.float32)

    for i in range(0, len(line)):
        line[i] = line[i].rstrip('\n')
        if len(line[i]) > 0:
            pos[i] = line[i].split()
        else:
            pos[i] = None

    Square = np.zeros([4])
    EpochNum = np.zeros([4])
    RMS = np.zeros([4])

    for j in range(0, 4):
        if len(pos) < 60:
            break
        elif len(pos) <= 2880:
            CalTimeSeries = range(60, len(pos))

        for i in CalTimeSeries:
            if pos[i, j + 11] != None and abs(pos[i, j + 11]) <= 0.1:
                Square[j] += (pos[i, j + 11]) ** 2
                EpochNum[j] += 1
        RMS[j] = math.sqrt(Square[j] / len(CalTimeSeries)) * 100
    UseRate = EpochNum[0] / len(CalTimeSeries)

    NumCover = 20
    for j in range(0, 4):
        for i in range(0, len(pos) - NumCover):
            nepo = 0
            for k in range(0, NumCover):
                if abs(pos[i + k, j + 11]) < 0.1:
                    nepo += 1
            if nepo == NumCover:
                converge_time[j] = i / 2
                break
    f.close()
    return converge_time, RMS, UseRate

def pos_split(posfile_path):
    posfile_list =[]
    for file in os.listdir(posfile_path):
        if '.pos' in file[-4:] and len(file) == 16:
            posfile_list.append(file)
    if posfile_list !=[] and not os.path.exists(posfile_path + "/hour"):
        os.mkdir(posfile_path + "/hour")
    for file in posfile_list:
        filepath = posfile_path + '//' + file
        f = open(filepath)
        lines = f.readlines()
        time = ['00', '04', '08', '12', '16', '20']
        index = range(0, 2881, 480)
        if len(lines) == 2880:
            for i in range(0, 6):
                filewpath = posfile_path + '//hour//' + file[:8] + time[i] + file[8:]
                fw = open(filewpath, 'w')
                for j in range(index[i], index[i+1]):
                    fw.write(lines[j])
    print('convert complete!')

def hourpos_calrms(posfile_path):
    folder = posfile_path + '//hour//'
    pos_list = []
    file_list = os.listdir(folder)
    for all_file in file_list:
        if all_file[-4:] == '.pos':
            pos_list.append(all_file)
    filepath = posfile_path.split('/')
    csv_file = filepath[-2] + '-' + filepath[-1] + '-' + 'ppp.csv'
    fs = open(posfile_path + '//' + csv_file, 'w', newline="")
    csv_write = csv.writer(fs)
    csv_write.writerow(['SiteName', 'HOUR', 'DOY', 'E', 'N', 'U', '3D', 'E', 'N', 'U', '3D', 'Use_Rate'])
    fs.close()
    for pos_file in pos_list:
        pos_path = folder + '/' + pos_file
        converge_time, RMS, UseRate = readPOS(pos_path)

        if np.isnan(RMS[0]) == 0 and RMS[0] != 0:
            fs = open(folder + '/../' + csv_file, 'a', newline="")
            csv_write = csv.writer(fs)
            csv_write.writerow([pos_file[0:4], pos_file[8:10], int(pos_file[4:7]), converge_time[0], converge_time[1],\
                                converge_time[2], converge_time[3], RMS[0], RMS[1], RMS[2], RMS[3], UseRate])
            fs.close()
    print('csv write complete!')


if __name__ == '__main__':
    # posfile_path = r'C:\Users\LZ\Desktop\arlz2\result\PPP_DYNAMIC_GC3'
    posfile_path = filedialog.askdirectory()
    pos_split(posfile_path)
    hourpos_calrms(posfile_path)




