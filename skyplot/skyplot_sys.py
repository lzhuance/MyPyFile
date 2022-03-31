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
    # 根据卫星id绘制单独的卫星轨迹
    for sys in sys_:
        data_ = data.loc[sys]

        ax.scatter(data_[data_.el <= elmask]["az"], data_[data_.el <= elmask]["el"], s=2, marker="o")
        ax.scatter(data_[data_.el > elmask]["az"], data_[data_.el > elmask]["el"], s=2, c='gray', marker="o")
        for prn in list(set(data_.prn.tolist())):
            id = "{}{:>02d}".format(sys, int(prn))
            ax.text(data_[data_.prn == prn]["az"][0], data_[data_.prn == prn]["el"][0], id, fontsize=12)

    # 绘制截止高度角圈
    theta = np.arange(0, 2 * np.pi, 0.02)
    ax.plot(theta, elmask * np.ones_like(theta), color='firebrick', lw=3)

    # 保存文件
    plt.savefig(sat_file + '.png', dpi=400)
    plt.show()


if __name__ == '__main__':
    sat_file = filedialog.askopenfilename(filetypes=[('txt', '*.txt'), ('All Files', '*')])
    data, sys_ = read_sat_info(sat_file)
    plot_sky(data, sys_, sat_file)
