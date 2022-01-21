# copyright
# @Pan Li. Email:lipan.whu@gmail.com
# @Jiahuan Hu. Email:hhu@whu.edu.cn

import math
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from tkinter import filedialog

class Satpos_base_t:
    def __init__(self):
        self.id = 'X00'
        self.csys  = 'X'
        self.prn   = 0
        self.lat   = 0.0
        self.lon   = 0.0
        self.h     = 0.0

class Satpos_1ep:
    def __init__(self):
        self.tm   = ''
        self.inf_fbs = []


def ecef2blh(x,y,z):
    e2=(1.0/298.257223563)*(2-(1.0/298.257223563))
    v=6378137.0
    r2=x*x+y*y

    b=math.atan(z/(math.sqrt(r2)))
    l=math.atan2(y,x)
    h=math.sqrt(r2+z*z)-v

    return b,l,h


def  readsp3file():
    filename = filedialog.askopenfilename( filetypes=[('sp3', '*.sp3'), ('All Files', '*')])
    fp=open(filename)
    f_Eps=[]
    ln=fp.readline()
    while ln:
        if '*' ==ln[0]:
            fEp=Satpos_1ep()
            while 1:
                ln=fp.readline()
                if not ln:
                    break
                if  '*' ==ln[0]:
                    break
                if 'P'!=ln[0]:
                    continue
                strs=ln.split()

                ss=strs[0][1:]
                ch=ss[0]
                prn=int(strs[0][2:])

                x=float(strs[1])*1000
                y=float(strs[2])*1000
                z=float(strs[3])*1000

                blh=ecef2blh(x,y,z)

                Satp=Satpos_base_t()
                Satp.id=ss
                Satp.sys=ch
                Satp.prn=prn
                Satp.lat=blh[0]*57.3
                Satp.lon=blh[1]*57.3
                Satp.h=blh[2]
                fEp.inf_fbs.append(Satp)

            f_Eps.append(fEp)


        else:
            ln=fp.readline()

    fp.close()
    return f_Eps


def draw_ground_track(Satposs):

    fig=plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.set_extent([-180, 180, -90, 90])

    latp=[]
    lonp=[]
    lat1=[]
    lon1=[]

    for fE0 in Satposs:
        for fb in fE0.inf_fbs:
            if fb.sys == 'G':
                if fb.prn<=32:
                    latp.append(fb.lat)
                    lonp.append(fb.lon)
                else:
                    lat1.append(fb.lat)
                    lon1.append(fb.lon)

    ax.scatter(lonp,latp,1,marker='o',color='brown',zorder=10)
    ax.scatter(lon1,lat1,1,marker='o',color='tomato',zorder=10)
    ax.gridlines(linestyle='--', draw_labels=True)

    plt.savefig('ground track1.tiff', dpi=400)
    plt.show()


if __name__ == "__main__":

    Satposs=readsp3file()
    draw_ground_track(Satposs)