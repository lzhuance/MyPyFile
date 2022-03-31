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
    sat = np.zeros((len(lines)-1, 4))
    satid = []
    time = []
    for i in range(1, len(lines)):
        ssat = lines[i].split()
        time.append(ssat[0]+' '+ssat[1])
        satid.append(ssat[2])
        sat[i-1] = [float(x) for x in ssat[3:]]
    f.close()
    data = pd.DataFrame(sat, columns=['az', 'el', 'snr', 'mp'], index=[satid, time])
    data.index.names = ['id', 'time']
    data["az"] = data["az"] / 180 * np.pi
    data["el"] = 90 - data["el"]
    satid_ = list(set(satid))
    return data, satid_

# 根据data绘制天空图
def plot_sky(data, satid_, sat_file):
    elmask = 90 - 20

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
    for id in satid_:
        data_ = data.loc[id]
        ax.scatter(data_[data_.el <= elmask]["az"], data_[data_.el <= elmask]["el"], s=2, marker="o")
        ax.scatter(data_[data_.el > elmask]["az"], data_[data_.el > elmask]["el"], s=2, c='gray', marker="o")
        ax.text(data_["az"][0], data_["el"][0], id, fontsize=12)

    # 绘制截止高度角圈
    theta = np.arange(0, 2 * np.pi, 0.02)
    ax.plot(theta, elmask * np.ones_like(theta), color='firebrick', lw=3)

    # 保存文件
    plt.savefig(sat_file + '.png', dpi=400)
    plt.show()


if __name__ == '__main__':
    sat_file = filedialog.askopenfilename(filetypes=[('txt', '*.txt'), ('All Files', '*')])
    data, satid_ = read_sat_info(sat_file)
    plot_sky(data, satid_, sat_file)
