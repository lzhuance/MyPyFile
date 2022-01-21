#!/usr/bin/python
# coding=utf-8

"""
gnss坐标转换库
Version：1.0
Author:LZ_CUMT
"""

from math import sin, cos, atan, pi, sqrt, atan2

# xyz转换为llh（经纬度）
def xyz2llh(ecef):
    aell = 6378137.0
    fell = 1.0 / 298.257223563
    deg = pi / 180
    u = ecef[0]
    v = ecef[1]
    w = ecef[2]
    esq = 2*fell-fell*fell
    lat = 0
    N = 0
    if w == 0:
        lat = 0
    else:
        lat0 = atan(w/(1-esq)*sqrt(u*u+v*v))
        j = 0
        delta = 10 ^ 6
        limit = 0.000001/3600*deg
        while delta > limit:
            N = aell / sqrt(1 - esq * sin(lat0)*sin(lat0))
            lat = atan((w / sqrt(u*u + v*v)) * (1 + (esq * N * sin(lat0) / w)))
            delta = abs(lat0 - lat)
            lat0 = lat
            j = j + 1
            if j > 10:
                break
    long = atan2(v, u)
    h = (sqrt(u*u+v*v)/cos(lat))-N
    llh = [lat * 180 / pi, long * 180 / pi, h]
    return llh

# 经纬度转化为xyz(参考RTKLIB)
def llh2xyz(llh):
    RE_WGS84 = 6378137.0
    FE_WGS84 = 1.0/298.257223563
    lat = llh[0] * pi / 180
    lon = llh[1] * pi / 180
    h = llh[2]
    sinp = sin(lat)
    cosp = cos(lat)
    sinl = sin(lon)
    cosl = cos(lon)
    e2 = FE_WGS84*(2.0-FE_WGS84)
    v = RE_WGS84 / sqrt(1.0 - e2 * sinp * sinp)
    x = (v+h)*cosp*cosl
    y = (v+h)*cosp*sinl
    z = (v*(1.0-e2)+h)*sinp
    return [x, y, z]


# xyz转换至以测站精确坐标为基准的enu坐标
def xyz2enu(xyz, basecrd):
    llhcrd = xyz2llh(basecrd)
    phi = llhcrd[0] * pi / 180
    lam = llhcrd[1] * pi / 180
    sinphi = sin(phi)
    cosphi = cos(phi)
    sinlam = sin(lam)
    coslam = cos(lam)
    difxyz = [xyz[0] - basecrd[0], xyz[1] - basecrd[1], xyz[2] - basecrd[2]]
    e = -sinlam*difxyz[0]+coslam*difxyz[1]
    n = -sinphi*coslam*difxyz[0]-sinphi*sinlam*difxyz[1]+cosphi*difxyz[2]
    u =  cosphi*coslam*difxyz[0]+cosphi*sinlam*difxyz[1]+sinphi*difxyz[2]
    return [e, n, u]
