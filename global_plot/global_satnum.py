# copyright
# @Pan Li. Email:lipan.whu@gmail.com
# @Jiahuan Hu. Email:hhu@whu.edu.cn

import os
import math
import numpy as np
#from mpl_toolkits.basemap import Basemap

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Satpos_base_t:
    def __init__(self):
        self.id = 'X00'
        self.csys  = 'X'
        self.prn   = 0
        self.x   = 0.0
        self.y   = 0.0
        self.z     = 0.0

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

def xyz2enu(b,l,h):
    sinp=math.sin(b)
    cosp=math.cos(b)
    sinl=math.sin(l)
    cosl=math.cos(l)
    E0=-sinl
    E1=-sinp*cosl
    E2=cosp*cosl
    E3=cosl
    E4=-sinp*sinl
    E5=cosp*sinl
    E6=0.0
    E7=cosp
    E8=sinp
    return E0,E1,E2,E3,E4,E5,E6,E7,E8

def ecef2enu(b,l,h,Ex,Ey,Ez):

    E=xyz2enu(b,l,h)
    ENUe=E[0]*Ex+E[3]*Ey+E[6]*Ez
    ENUn=E[1]*Ex+E[4]*Ey+E[7]*Ez
    ENUu=E[2]*Ex+E[5]*Ey+E[8]*Ez
    return ENUe,ENUn,ENUu



def pos2ecef(b,l,h):
    sinp=math.sin(b)
    cosp=math.cos(b)
    sinl=math.sin(l)
    cosl=math.cos(l)
    e2=(1.0/298.257223563)*(2-(1.0/298.257223563))
    v=6378137.0/math.sqrt(1-e2*sinp*sinp)

    x=(v+h)*cosp*cosl
    y=(v+h)*cosp*sinl
    z=(v*(1-e2)+h)*sinp

    return x,y,z


def averagenum(num):
    nsum=0
    for i in range(len(num)):
        nsum+=num[i]

    return nsum/len(num)


def  readsp3file():
    fp=open('gbm21384.SP3')
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

                Satp=Satpos_base_t()
                Satp.id=ss
                Satp.sys=ch
                Satp.prn=prn
                Satp.x=x
                Satp.y=y
                Satp.z=z
                fEp.inf_fbs.append(Satp)
            f_Eps.append(fEp)
        else:
            ln=fp.readline()
    fp.close()
    return f_Eps


def count_ns_grid(Satposs,lon,lat):

    b = lat*(math.pi/180)
    l = lon*(math.pi/180)
    h = 0
    Rexyz=pos2ecef(b,l,h)
    Rx=Rexyz[0]
    Ry=Rexyz[1]
    Rz=Rexyz[2]

    To_nsat=[]
    EP_nsat=[]
    for fE0 in Satposs:
        n_sat = 0
        i=0
        for fb in fE0.inf_fbs:
            if fb.sys=='J'or fb.sys=='G':
            #if fb.sys=='C'or fb.sys=='G':
                #if fb.prn!=59 & fb.prn!=60:
                #if fb.prn <=16:
                    i+=1
                    Sx=fb.x
                    Sy=fb.y
                    Sz=fb.z

                    r = math.sqrt((Rx-Sx) * (Rx-Sx) + (Ry-Sy) * (Ry-Sy) +(Rz-Sz) * (Rz-Sz))

                    Ex=(Sx-Rx)/r
                    Ey=(Sy-Ry)/r
                    Ez=(Sz-Rz)/r

                    ENU=ecef2enu(b,l,h,Ex,Ey,Ez)
                    #el=math.asin(ENU[2])
                    #el = math.atan(ENU[2]/math.sqrt(ENU[0]**2+ENU[1]**2))
                    #if el>0.0:
                    if ENU[2] > 0.0:
                        n_sat=n_sat+1
                    else:
                        continue


        EP_nsat.append(n_sat)
    E_nsat=averagenum(EP_nsat)
    return E_nsat


if __name__ == "__main__":

    Satposs=readsp3file()


    Total=[]

    data=open("gps_qzss_sat.txt",'w+')

    for lat in range(90,-90,-2):
        N_sat = []
      #  i=int((lon+180)/30)
        for lon in range(-180, 180, 5):
            nsat=count_ns_grid(Satposs,lon,lat)
            print('%.2f' % nsat,file=data,end=" ")
            N_sat.append(nsat)
            print(lon,lat,nsat)
        print('\n',file=data)
        Total.append(N_sat)
  #  print(N_sat)
    data.close()

pllon=np.arange(-180,180,5)
pllat=np.arange(90,-90,-2)
grid_lon,grid_lat=np.meshgrid(pllon,pllat)

fig = plt.figure(figsize=(16, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

cs=ax.contourf(grid_lon, grid_lat, Total,cmap=plt.cm.jet,vmin=0, vmax=16)

ax.coastlines()

plt.colorbar(cs,ax=ax)


#ax.gridlines(linestyle='--', draw_labels=True)
#plt.title('GPS')
plt.savefig('gps_qzss-satnum.jpg', dpi=400)
#plt.show()



