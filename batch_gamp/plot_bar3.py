# coding=utf-8
# !/usr/bin/env python
'''
 Program:
 Author:LZ_CUMT
 Version:1.0
 Date:2021/10/10
 '''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


if __name__ == '__main__':
    filepath=r"C:\Users\LZ\Desktop\isb\pos0.csv"
    filepath2 = r"C:\Users\LZ\Desktop\isb\pos1.csv"
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 10.5,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    #fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    fig = plt.figure()

    ax1 = plt.subplot(211)
    f = open(filepath, 'r')
    ln = f.readline()
    site = []
    pose = []
    posn = []
    posu = []

    while ln:
        ln = f.readline()
        if not ln:
            break
        str = ln.split(',')
        site.append(str[0].upper())
        pose.append(float(str[1]))
        posn.append(float(str[2]))
        posu.append(float(str[3]))
    index = np.arange(19)
    bar_width = 0.25
    for i in range(len(site)):
        print(site[i],pose[i],posn[i],posu[i])
    rects1 = ax1.bar(index - bar_width * 0.5, pose, bar_width, alpha=0.4, color='b', label='E')
    rects2 = ax1.bar(index + bar_width * 0.5, posn, bar_width, alpha=0.4, color='r', label='N')
    rects3 = ax1.bar(index + bar_width * 1.5, posu, bar_width, alpha=0.4, color='g', label='U')
    #ax1.set_xticks(index + bar_width / 2)
    plt.yticks(fontsize='large')
    #ax1.set_xticklabels(site, fontsize='x-large')
    plt.legend(fontsize='x-large',loc='upper right')
    #plt.ylabel('Convergence Time[min]', fontsize='x-large')
    plt.ylabel('位置误差[cm]', fontsize='x-large')
    #plt.ylabel('Positioning Accuracy[cm]', fontsize='x-large')
    #plt.xlabel('Site', fontsize='x-large')
    plt.xlabel('站点', fontsize='x-large')
    plt.ylim([0, 4.5])
    plt.text(-1,3.8,'ISB OFF',fontsize='xx-large')
    #plt.ylim([0, 120])
    #plt.tight_layout()


    f1 = open(filepath2, 'r')
    ln1 = f1.readline()
    site1 = []
    pose1 = []
    posn1 = []
    posu1 = []

    while ln1:
        ln1 = f1.readline()
        if not ln1:
            break
        str = ln1.split(',')
        site1.append(str[0].upper())
        pose1.append(float(str[1]))
        posn1.append(float(str[2]))
        posu1.append(float(str[3]))

    for i in range(len(site1)):
        print(site1[i],pose1[i],posn1[i],posu1[i])

    #fig, ax = plt.subplots(figsize=(6,4))
    index = np.arange(19)
    bar_width = 0.25
    ax2 = plt.subplot(212, sharex=ax1)
    rects1 = ax2.bar(index - bar_width*0.5, pose1, bar_width, alpha=0.4, color='b', label='E')
    rects2 = ax2.bar(index + bar_width*0.5, posn1, bar_width, alpha=0.4, color='r', label='N')
    rects3 = ax2.bar(index + bar_width*1.5, posu1, bar_width, alpha=0.4, color='g', label='U')
    ax2.set_xticks(index + bar_width / 2)
    plt.yticks(fontsize='large')
    ax2.set_xticklabels(site,fontsize='x-large')
    #plt.legend(fontsize='x-large')
    #plt.ylabel('Convergence Time[min]',fontsize='x-large')
    plt.ylabel('位置误差[cm]', fontsize='x-large')
    #plt.ylabel('Positioning Accuracy[cm]', fontsize='x-large')
    #plt.xlabel('Site',fontsize='x-large')
    plt.xlabel('站点', fontsize='x-large')
    plt.ylim([0,4.5])
    plt.text(-1, 3.8, 'ISB ON', fontsize='xx-large')
    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    ax1.get_shared_x_axes().join(ax1, ax2)
    #ax1.set_xticklabels([])

    plt.savefig(filepath + '.bar1.png', dpi=600)
    plt.show()