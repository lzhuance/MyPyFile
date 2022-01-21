# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''

import matplotlib.pyplot as plt
import os

def readstat(file, i):
    color = ['r', 'b', 'g']
    plus = [0, 0, 0]
    f = open(file)
    site = file[-21:]
    ln = f.readline()
    bdisb = []
    while ln:
        ln = f.readline()
        if '$CLK' in ln:
            sp = ln.split(',')
            gclk = float(sp[5])
            b2clk = float(sp[7])
            eclk = float(sp[8])
            b3clk = float(sp[10])+plus[i]
            #.append(b2clk-b3clk)
            bdisb.append(b3clk)
    if bdisb != []:
        print(site)
        plt.plot(bdisb,'-o',lw=0.5,markersize=1, color = color[i])
        #print(bdisb[0:100])


if __name__ == '__main__':
    # file1 = r'D:\paperdata\result1\ppp_static_C2C3_TC\metg1830.21o.pos.stat'
    # file2 = r'D:\paperdata\result1\ppp_static_C2C3_RW\metg1830.21o.pos.stat'
    # file3 = r'D:\paperdata\result1\ppp_static_C2C3_WN\metg1830.21o.pos.stat'
    # file1 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_TC\abpo0010.20o.pos.stat'
    # file2 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_RW\abpo0010.20o.pos.stat'
    # file3 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_WN\abpo0010.20o.pos.stat'
    # file4 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_off\abpo0010.20o.pos.stat'
    filepath = r'D:\paperdata\result11'
    path_list = ['ppp_kine_C2C3_TC', 'ppp_kine_C2C3_RW', 'ppp_kine_C2C3_WN']
    for i in range(3):
        path_list[i] = filepath + '//' + path_list[i]
    stat_list = os.listdir(path_list[0])
    index = 0
    for stat_file in stat_list:
        if '.stat' in stat_file:
            index += 1
            plt.figure(num=index)
            for i in range(3):
                stat_path = path_list[i] + '//' + stat_file
                readstat(stat_path, i)
            plt.legend(['TC', 'RW', 'WN'])
            plt.xlabel('Time',fontsize='x-large')
            plt.ylabel('ISB[ns]',fontsize='x-large')
            plt.title(stat_path[-21:-17], fontsize='xx-large')
            plt.xlim(0, 2880)
            plt.yticks(fontsize='large')
            plt.xticks([0, 720, 1440, 2160, 2880], ['00:00', '06:00', '12:00', '18:00', '00:00'],fontsize='large')
            plt.savefig(filepath + '//png//' + stat_file + '.png')
            #plt.show()
'''
    readstat(file1)
    readstat(file2)
    readstat(file3)
    #readstat(file4)
    plt.legend(['TC','RW','WN'])
    plt.xlabel('Time')
    plt.ylabel('ISB[ns]')
    plt.xticks([0, 720, 1440, 2160, 2880], ['00:00', '06:00', '12:00', '18:00', '00:00'])
    plt.show()
'''
