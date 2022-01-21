#!/usr/bin/python
# coding=utf-8

import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

def plotenu(pos,epoch,num,pos_file):
    ylib = np.linspace(-1, 1, 11)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(epoch, pos[:, 11:14])
    ax.grid(True, linestyle='--')
    if num > 0:
        ax.axis([0, num, -1, 1])
    ax.set_yticks(ylib)

    plt.title(pos_file[0:4].upper())
    plt.ylabel('Error[m]')
    plt.xlabel('Epoch')

    plt.text(1000, -0.55, ' Covengence Time', fontsize=12)
    plt.text(1000, -0.65, 'E: ' + str(converge_time[0]) + 'min', fontsize=12)
    plt.text(1000, -0.75, 'N: ' + str(converge_time[1]) + 'min', fontsize=12)
    plt.text(1000, -0.85, 'U: ' + str(converge_time[2]) + 'min', fontsize=12)
    plt.text(1000, -0.95, '3D:' + str(converge_time[3]) + 'min', fontsize=12)

    plt.text(2000, -0.55, 'Positioning RMS', fontsize=12)
    plt.text(2000, -0.65, 'E :' + str(RMS[0])[0:5] + 'm', fontsize=12)
    plt.text(2000, -0.75, 'N :' + str(RMS[1])[0:5] + 'm', fontsize=12)
    plt.text(2000, -0.85, 'U :' + str(RMS[2])[0:5] + 'm', fontsize=12)
    plt.text(2000, -0.95, '3D:' + str(RMS[3])[0:5] + 'm', fontsize=12)

    plt.legend(['E', 'N', 'U'])

    plt.savefig(folder + '/' + pos_file + '.png', dpi=400)
    plt.close()
    plt.show()

def readPOS(PosFile):
    converge_time = np.zeros([4], dtype=np.float32)
    UseRate = 1
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
        CalTimeSeries = range(0, len(pos))
        for i in CalTimeSeries:
            if pos[i, j + 11] != None:
                Square[j] += (pos[i, j + 11]) ** 2
                EpochNum[j] += 1
        RMS[j] = math.sqrt(Square[j] / len(pos))


    f.close()
    return converge_time, RMS, UseRate

def readPDOP(PdopFile):
    f = open(PdopFile, 'r')
    line = f.readlines()
    num = len(line)
    pdop = np.zeros([num, 16], dtype=np.float32)

    for i in range(0, len(line)):
        line[i] = line[i].rstrip('\n')
        if len(line[i]) > 0:
            pdop[i] = line[i].split()
        else:
            pdop[i] = None
    mean_pdop = np.mean(pdop, 0)
    site_pdop = mean_pdop[15]
    sat_num = mean_pdop[8]
    f.close()
    return site_pdop, sat_num


if __name__ == '__main__':
    pos_list = []
    folder = filedialog.askdirectory()
    file_list = os.listdir(folder)
    for all_file in file_list:
        if all_file[-4:] == '.pos':
            pos_list.append(all_file)
    filepath = folder.split('/')
    csv_file = filepath[-2] + '-' + filepath[-1] + '-' + 'ppp.csv'
    fs = open(folder + '/../' + csv_file, 'w', newline="")
    csv_write = csv.writer(fs)
    csv_write.writerow(['SiteName', 'DOY', 'E', 'N', 'U', '3D', 'E', 'N', 'U', '3D', 'Use_Rate'])
    # csv_write.writerow(['SiteName', 'DOY', 'E', 'N', 'U', '3D', 'E', 'N', 'U', '3D', 'Use_Rate', 'PDOP', 'SatNum'])
    fs.close()
    # Num = 0
    for pos_file in pos_list:
        # Num += 1
        # print('*************** Processing the '+str(Num)+'th file ***************')
        # print(foldername+'/'+filename)
        pos_path = folder + '/' + pos_file
        pdop_path = folder + '/' + pos_file[:-3] + "pdop"
        converge_time, RMS, UseRate = readPOS(pos_path)
        #pdop, SatNum = readPDOP(pdop_path)
        # plotenu(pos,epoch,num)

        #if UseRate == 1 and np.isnan(RMS[0]) == 0 and RMS[0] != 0 and pdop < 4:
        if UseRate == 1 and np.isnan(RMS[0]) == 0 and RMS[0] != 0 :
            fs = open(folder + '/../' + csv_file, 'a', newline="")
            csv_write = csv.writer(fs)
            csv_write.writerow([pos_file[0:4], int(pos_file[4:7]), converge_time[0], converge_time[1], converge_time[2], \
                                converge_time[3], RMS[0], RMS[1], RMS[2], RMS[3], UseRate])
            #                    converge_time[3], RMS[0], RMS[1], RMS[2], RMS[3], UseRate, pdop, SatNum])
            fs.close()
