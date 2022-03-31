# coding=utf-8
# !/usr/bin/env python
'''
 Program:skyplot
 Author:LZ_CUMT
 Version:2.0
 Date:2022/03/27
 '''
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
import pandas as pd


# 读取rtklib导出卫星信息，转换为Dataframe
def read_sat_info(sat_file):
    f = open(sat_file, 'r')
    lines = f.readlines()
    sat = np.zeros((len(lines)-1, 5))
    sys = []
    time = []
    for i in range(1, len(lines)):
        ssat = lines[i].split()
        time.append(ssat[0]+' '+ssat[1])
        sys.append(ssat[2][0])
        sat[i-1, 0] = int(ssat[2][1:])
        sat[i-1, 1:] = [float(x) for x in ssat[3:]]
    f.close()
    data = pd.DataFrame(sat, columns=['prn', 'az', 'el', 'snr', 'mp'], index=[sys, time])
    data.index.names = ['sys', 'time']
    data["az"] = data["az"] / 180 * np.pi
    data["el"] = 90 - data["el"]
    data["mp"] = abs(data["mp"])
    sys_ = list(set(sys))
    return data, sys_

# 根据data绘制天空图
def plot_sky(data, sys_, sat_file):
    elmask = 90 +10

    # 极坐标及底图设置
    ax = plt.subplot(111, projection='polar')
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    ax.set_rlim([0, 90])
    ax.set_rticks([0, 30, 60, 90])
    ax.yaxis.set_label_position('right')
    ax.tick_params('y', labelleft=False)
    plt.grid(linestyle="--")

    SATAZ = [0, 0, 0 ]
    SATEL = [0, 30, 60]
    SATID = ['90°', '60°', '30°']
    for i in range(0, 3):
        ax.text(SATAZ[i], SATEL[i], SATID[i])

    cm = plt.get_cmap('viridis_r')
    sc = ax.scatter(data[data.snr>10]["az"], data[data.snr>10]["el"], c=data[data.snr>10]["snr"], cmap=cm,zorder=0, s=1)
    cb = plt.colorbar(sc)
    cb.set_label('L1 SNR[dB-Hz]')
    # 保存文件
    plt.savefig(sat_file + '.png', dpi=400)
    plt.show()


if __name__ == '__main__':
    sat_file = filedialog.askopenfilename(filetypes=[('txt', '*.txt'), ('All Files', '*')])
    data, sys_ = read_sat_info(sat_file)
    plot_sky(data, sys_, sat_file)
