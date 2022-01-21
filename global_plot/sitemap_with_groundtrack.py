

import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

def paint(Satposs):
    mpl.rcParams['font.sans-serif'] = ['Helvetical']
    mpl.rcParams['axes.unicode_minus'] = False
    mpl.rc('xtick', labelsize=9)
    mpl.rc('ytick', labelsize=9)
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    plt.rcParams['savefig.dpi'] = 300

    mgex = np.recfromcsv('station_ppp.csv', names=True)

    fig = plt.figure(figsize=(6.4, 3.2))
    # Set projection
    ax = plt.axes(projection=ccrs.PlateCarree())
    # Add ocean and land
    ax.set_extent([60,180, 10, 50], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.1)
    sites = ['JFNG', 'GMSD', 'USUD']
    # Add MGEX & IGS core sites
    ax.plot(mgex['long'], mgex['lat'], 'o', color='firebrick',mec='k',mew=0.5, transform=ccrs.Geodetic(), ms=10.0)

    latp=[]
    lonp=[]
    lat1=[]
    lon1=[]

    for fE0 in Satposs:
        for fb in fE0.inf_fbs:
            if fb.sys == 'J':
                if fb.prn<=10:
                    latp.append(fb.lat)
                    lonp.append(fb.lon)
                else:
                    lat1.append(fb.lat)
                    lon1.append(fb.lon)

    ax.scatter(lonp,latp,1,marker='o',color='seagreen',zorder=1)

    #ax.scatter(lon1,lat1,1,marker='o',color='tomato',zorder=10)
    #ax.gridlines(linestyle='--', draw_labels=True)
    plt.text(114.491-17,30.516-4, 'JFNG', transform=ccrs.Geodetic(), FontSize=10)
    plt.text(131.016-13,30.556-9, 'GMSD', transform=ccrs.Geodetic(), FontSize=10)
    plt.text(101.507 - 13, 2.784- 9, 'ANMG', transform=ccrs.Geodetic(), FontSize=10)
    plt.text(131.133 , -12.844 - 9, 'DARW', transform=ccrs.Geodetic(), FontSize=10)
    plt.text(141.133 +3, 39.135 +3, 'MIZU', transform=ccrs.Geodetic(), FontSize=10)
    plt.text(147.366 +3, -2.043 +3, 'PNGM', transform=ccrs.Geodetic(), FontSize=10)

    ax.set_xticks([60,100, 140,180], crs=ccrs.PlateCarree())
    ax.set_yticks([-50,-25,0,25,50], crs=ccrs.PlateCarree())
    #ax.gridlines(linestyle='--', linewidth=1.0)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)




    fig.savefig('PPP.tiff', bbox_inches='tight', dpi=300)
    plt.show()

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
    fp=open('gbm21220.SP3')
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

    #fig=plt.figure()
    #ax = plt.axes(projection=ccrs.PlateCarree())
    #ax.add_feature(cfeature.LAND)
    #ax.add_feature(cfeature.OCEAN)
    #ax.set_extent([-180, 180, -90, 90])

    #mymap=Basemap()
    #mymap.fillcontinents(color='white', lake_color='lightskyblue')
    #mymap.drawmapboundary(fill_color='skyblue')
    #mymap.drawcoastlines()
    #mymap.drawcountries()

    latp=[]
    lonp=[]
    lat1=[]
    lon1=[]

    #latp=np.zeros((61,298))
    #lonp=np.zeros((61,298))
    #n=0
    #for fE0 in Satposs:
    #    n=n+1
    #    for fb in fE0.inf_fbs:
    #        if fb.sys == 'C':
    #            latp[fb.prn,n]=fb.lat
    #            lonp[fb.prn,n]=fb.lon

    #lonp.sort(axis=1)
    #latp.sort(axis=1)
    #for i in range(1, 61):
    #        ax.plot(lonp[i], latp[i], 1, '--', color='r', zorder=30)
#    for i in range(1,61):
#        for j in range(0, 288):
#            if lonp[i,j]!=0:
#                if abs(lonp[i,j]-lonp[i,j+1])<200:
#                    ax.plot(lonp[i,j:j+1], latp[i,j:j+1], 1, '--', color='r', zorder=30)
    for fE0 in Satposs:
        for fb in fE0.inf_fbs:
            if fb.sys == 'C':
                if fb.prn<=16:
                    latp.append(fb.lat)
                    lonp.append(fb.lon)
                else:
                    lat1.append(fb.lat)
                    lon1.append(fb.lon)

    #ax.scatter(lonp,latp,1,marker='o',color='brown',zorder=10)
    #ax.scatter(lon1,lat1,1,marker='o',color='tomato',zorder=10)
    #ax.gridlines(linestyle='--', draw_labels=True)

    plt.savefig('ground track2.tiff', dpi=400)
    plt.show()


if __name__ == "__main__":

    Satposs=readsp3file()
    paint(Satposs)
