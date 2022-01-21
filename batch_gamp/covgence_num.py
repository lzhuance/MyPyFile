#!/usr/bin/python
# coding=utf-8
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes=[('csv', '*.csv'), ('All Files', '*')])
    f = open(filename, 'r')
    ln = f.readline()
    covtimes = []
    while ln:
        ln = f.readline()
        if not ln:
            break
        str = ln.split(',')
        covtime = float(str[5])
        covtimes.append(covtime)
    if 1:
        gap = [10, 20, 30, 40, 50, 60]
        gapp = [0, 10, 20, 30, 40, 50, 60]
    else:
        gap = [15, 30, 45, 60, 75, 90]
        gapp = [0, 15, 30, 45, 60, 75, 90]
    count = [0, 0, 0, 0, 0, 0, 0]
    for i in covtimes:
        if i < gap[0]:
            count[0] += 1
        elif i < gap[1]:
            count[1] += 1
        elif i < gap[2]:
            count[2] += 1
        elif i < gap[3]:
            count[3] += 1
        elif i < gap[4]:
            count[4] += 1
        elif i < gap[5]:
            count[5] += 1
        else:
            count[6] += 1
    for j in range(0, 7):
        count[j] = count[j]/len(covtimes)*100
    plt.bar(np.arange(-0.5, 6.5, 1), count, width=1)
    plt.xticks(ticks=range(-1, 6), labels=gapp)
    plt.xlim(-1, 6)
    plt.xlabel('Covergence Time[min]')  # title of x axis
    plt.ylabel('Percent (%)')
    plt.show()
    plt.savefig(filename + '.percent.png', dpi=600)
