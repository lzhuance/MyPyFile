# coding=utf-8
# !/usr/bin/env python
'''
 Program: mobile_enu
 Author:LZ_CUMT
 Version:2.0
 Date:2021/12/1
 '''
from gnss_cmn.crd_conv import xyz2enu
from gnss_cmn.time_conv import ymdhms2wksow
import matplotlib.pyplot as plt
import math
from matplotlib import rcParams

def read_RTKLIB_pos(file):
    xyzlist = []
    f = open(file)
    return xyzlist

def read_GAMP_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if len(ln) > 10:
            x = float(ln[36:49])
            y = float(ln[51:64])
            z = float(ln[66:79])
            t = int(ln[25:31])
            xyzlist.append([x, y, z, t])
        ln = f.readline()
    print("[INFO] Finish Reading the GAMP pos file")
    return xyzlist

def read_NetDiff_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if ln[0] != '%':
            x = float(ln[76:88])
            y = float(ln[91:103])
            z = float(ln[106:118])
            year = int(ln[0:4])
            mouth = int(ln[5:7])
            day = int(ln[8:10])
            hour = int(ln[11:13])
            mini = int(ln[14:16])
            sec = int(ln[17:19])
            week, t = ymdhms2wksow(year, mouth, day, hour, mini, sec)
            xyzlist.append([x, y, z, t])
        ln = f.readline()
    print("[INFO] Finish Reading the Net_Diff pos file")
    return xyzlist

def read_IE_POS(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        ln = f.readline()
        if ln[3:10] == "(weeks)":
            break
    while ln:
        ln = f.readline()
        if not ln:
            break
        if ln[18:21] == "000":
            x = float(ln[22:36])
            y = float(ln[37:51])
            z = float(ln[52:66])
            t = int(ln[11:17])
            xyzlist.append([x, y, z, t])
    print("[INFO] Finish Reading the IE pos file")
    return xyzlist

def math_rms(enu):
    sump = [0, 0, 0]
    rms = []
    for i in range(len(enu[0])):
        for j in range(len(enu)):
            sump[i] += enu[j][i] * enu[j][i]
        rms.append(round(math.sqrt(sump[i] / len(enu)), 2))
    return rms


if __name__ == '__main__':
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 10.5,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    mode =0   # [ 0:static 1:daynamic ]
    enu = []
    enu1 = []
    pngfile = r'C:\Users\LZ\Desktop\mobile2\result\hel\spp_el_hel_C2C3.png'
    # static mode with one pos file and the coordinate
    if mode == 0:
        file1 = r'C:\Users\LZ\Desktop\mobile2\result\hel\spp_el_hel0_C2C3\static.21o.pos'
        file2 = r'C:\Users\LZ\Desktop\mobile2\result\hel\spp_el_hel_C2C3\static.21o.pos'
        xyz = [-2408833.3756, 4698173.9885, 3566552.9386]  # change the coordinate [X, Y, Z]
        list = read_GAMP_pos(file1)
        for i in range(len(list)):
            if list[i] != []:
                print(xyz2enu(list[i][0:3], xyz))
                enu.append(xyz2enu(list[i][0:3], xyz))
        list1 = read_GAMP_pos(file2)
        for i in range(len(list1)):
            if list1[i] != []:
                print(xyz2enu(list1[i][0:3], xyz))
                enu1.append(xyz2enu(list1[i][0:3], xyz))
    # dynamic mode with one rover pos file and one base pos file
    if mode == 1:
        # change the pos file path
        file1 = r'C:\Users\LZ\Desktop\mobile2\result\spp_ele_15_GC\daynamic.21o.pos'
        file2 = r'C:\Users\LZ\Desktop\mobile2\Coor_2021280_base-rove.pos'
        # file1 = r'C:\Users\LZ\Desktop\IRTK\PPP\Coor_2021196_KVH0-KVH0.pos'
        # file2 = r'C:\Users\LZ\Desktop\IRTK\Coor_2021196_base-KVH0.pos'
        # file2 = r'C:\Users\LZ\Desktop\RTK-INS-2021196\2021196-LC.txt'

        # choose the pos file format
        list1 = read_GAMP_pos(file1)
        list2 = read_NetDiff_pos(file2)
        # list2 = read_IE_POS(file2)

        ind1 = 0
        ind2 = 0
        while ind1 < len(list1) and ind2 < len(list2):
            if list1[ind1][3] == list2[ind2][3]:
                enu.append(xyz2enu(list1[ind1][0:3], list2[ind2][0:3]))
                ind1 += 1
                ind2 += 1
            elif list1[ind1][3] > list2[ind2][3]:
                ind2 += 1
            elif list1[ind1][3] < list2[ind2][3]:
                ind1 += 1
    e = []
    n = []
    u = []
    e1 = []
    n1 = []
    u1 = []
    for i in range(len(enu)):
        e.append(enu[i][0])
        n.append(enu[i][1])
        u.append(enu[i][2])
        e1.append(enu1[i][0])
        n1.append(enu1[i][1])
        u1.append(enu1[i][2])
    if mode == 0 or mode == 1:
        rms = math_rms(enu)
        rms1 = math_rms(enu1)
        #print(rms)

        plt.figure(figsize=(8,6))
        plt.subplot(3, 1, 1)
        plt.plot(e, lw=0.8, color='r')
        plt.plot(e1, lw=0.8, color='b')
        plt.ylim(-23, 23)
        plt.yticks([-20, -10, 0, 10, 20], fontsize='x-large')
        plt.xticks([])
        plt.ylabel('E方向误差[m]', fontsize='x-large')
        plt.xlim(0, len(e))
        plt.text(15, 18, 'RMS1 = ' + str(rms[0]) + ' m', fontsize='x-large')
        plt.text(1015, 18, 'RMS2 = ' + str(rms1[0]) + ' m', fontsize='x-large')
        plt.legend(['Helmert OFF', 'Helmert ON'], fontsize='large', loc='upper right')

        plt.subplot(3, 1, 2)
        plt.plot(n, lw=0.8, color='r')
        plt.plot(n1, lw=0.8, color='b')
        plt.yticks([-20, -10, 0, 10, 20], fontsize='x-large')
        plt.xticks([])
        plt.ylabel('N方向误差[m]', fontsize='x-large')
        plt.ylim(-23, 23)
        plt.xlim(0, len(e))
        plt.text(15, 18, 'RMS1 = ' + str(rms[1]) + ' m', fontsize='x-large')
        plt.text(1015, 18, 'RMS2 = ' + str(rms1[1]) + ' m', fontsize='x-large')

        plt.subplot(3, 1, 3)
        plt.plot(u, lw=0.8, color='r')
        plt.plot(u1, lw=0.8, color='b')
        plt.yticks([-30, -20, -10, 0, 10, 20,30], fontsize='x-large')
        plt.ylabel('U方向误差[m]', fontsize='x-large')
        plt.ylim(-33, 33)
        plt.xlim(0, len(e))
        plt.xticks(fontsize='x-large')
        plt.text(15, 26, 'RMS1 = ' + str(rms[2]) + ' m', fontsize='x-large')
        plt.text(1015, 26, 'RMS2 = ' + str(rms1[2]) + ' m', fontsize='x-large')
        #plt.grid(b=1, ls='--')
        #plt.title(rms)

        plt.xlabel('历元', fontsize='x-large')
        #plt.ylabel('Error[m]')
        #plt.ylim([-10, 10])
        plt.subplots_adjust(hspace=0)

        plt.savefig(pngfile, dpi=600)
        plt.show()
        print("[INFO] Finish the paint")

