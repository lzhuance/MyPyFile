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


def read_csv(filepath):
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

    for i in range(len(site)):
        print(site[i],pose[i],posn[i],posu[i])

    #fig, ax = plt.subplots(figsize=(6,4))
    index = np.arange(19)
    bar_width = 0.25
    ax1 = plt.subplot(211)
    rects1 = ax.bar(index - bar_width*0.5, pose, bar_width, alpha=0.4, color='b', label='E')
    rects2 = ax.bar(index + bar_width*0.5, posn, bar_width, alpha=0.4, color='r', label='N')
    rects3 = ax.bar(index + bar_width*1.5, posu, bar_width, alpha=0.4, color='g', label='U')
    ax.set_xticks(index + bar_width / 2)
    plt.yticks(fontsize='large')
    ax.set_xticklabels(site,fontsize='x-large')
    plt.legend(fontsize='x-large')
    plt.ylabel('Convergence Time[min]',fontsize='x-large')
    #plt.ylabel('收敛时间[min]')
    #plt.ylabel('Positioning Accuracy[cm]')
    plt.xlabel('Site',fontsize='x-large')
    #plt.xlabel('站点')
    plt.ylim([0,120])
    plt.tight_layout()

    plt.savefig(filepath + '.bar1.png', dpi=600)
    plt.show()


if __name__ == '__main__':
    filepath=r"C:\Users\LZ\Desktop\isb\con00.csv"
    filepath2 = r"C:\Users\LZ\Desktop\isb\con01.csv"
    config = {
        "font.family": 'serif',  # 衬线字体
        "font.size": 10.5,  # 相当于小四大小
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['STSong'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    #rcParams.update(config)
    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
    read_csv(filepath)
    read_csv(filepath2)