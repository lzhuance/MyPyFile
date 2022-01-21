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

def readstat(file,loc):
    f = open(file)
    site = file[-21:-17]
    doy = int(file[-17:-14])
    ln = f.readline()
    bdisb = []
    while ln:
        ln = f.readline()
        if '$CLK' in ln:
            sp = ln.split(',')
            gclk = float(sp[5])
            b2clk = float(sp[7])
            eclk = float(sp[8])
            b3clk = float(sp[10])
            #.append(b2clk-b3clk)
            bdisb.append(b3clk)
    if bdisb != []:
        sum = 0
        for i in range(60,len(bdisb)):
            sum += bdisb[i]
        ave = sum/(len(bdisb)-60)
        print(site,doy,ave)
        loc.append([site,doy,ave*0.3])
        #print(bdisb[0:100])


if __name__ == '__main__':
    # file1 = r'D:\paperdata\result1\ppp_static_C2C3_TC\metg1830.21o.pos.stat'
    # file2 = r'D:\paperdata\result1\ppp_static_C2C3_RW\metg1830.21o.pos.stat'
    # file3 = r'D:\paperdata\result1\ppp_static_C2C3_WN\metg1830.21o.pos.stat'
    # file1 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_TC\abpo0010.20o.pos.stat'
    # file2 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_RW\abpo0010.20o.pos.stat'
    # file3 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_WN\abpo0010.20o.pos.stat'
    # file4 = r'C:\Users\LZ\Desktop\arlz\result1\ppp_static_GE_off\abpo0010.20o.pos.stat'
    path_list = r'D:\paperdata\result111\ppp_static_C2C3_RW'
    stat_list = os.listdir(path_list)
    index = 0
    loc = []
    for stat_file in stat_list:
        if '.stat' in stat_file:
            index += 1
            #plt.figure(num=index)
            stat_path = path_list + '//' + stat_file
            readstat(stat_path,loc)
    #sites = ['cusv','krgg','ptgg','wtzr']
    sites = ['cusv', 'krgg']
    for site1 in sites:
        isb = []
        for j in range(len(loc)):
            if loc[j][0] == site1:
                isb.append(loc[j][2])
        if isb != []:
            plt.plot(isb)
    plt.show()
