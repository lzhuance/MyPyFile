#!/usr/bin/python
# coding=utf-8
"""
Net_Diff POS文件转换至ENU误差并绘图
Version：1.0
Author:LZ_CUMT
脚本功能：
1：读取Net_Diff解算结果文件（.pos)，并将XYZ或LLH坐标转换为ENU形式
2：转换时选取的坐标基准通过snx文件进行读取，若snx文件中无当前测站或未找到snx文件，以定位结果的均值作为替代
3：转换完成后将ENU输出至csv格式文件保存，通过matplotlib库（需额外安装）绘制ENU定位误差图
"""



import csv
from math import sin, cos, atan, pi, sqrt, atan2, floor
import matplotlib.pyplot as plt

# 年月日转换为儒略日
def ymd2mjd(year, mm, dd):
    if mm <= 2:
        mm += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += floor(30.6001 * (mm + 1)) + 2.0 - floor(year / 100.0) + floor(year / 400) + dd
    return mjd

# 年月日转换为GPS周及周内天
def ymd2wkdow(year, mm, dd):
    mjd0 = 44243
    mjd = ymd2mjd(year, mm, dd)
    difmjd = mjd-mjd0-1
    week = floor(difmjd / 7)
    dow = floor(difmjd % 7)
    return week, dow

def ymdhms2wksow(year, month, day, hour, min, sec):
    week, dow = ymd2wkdow(year, month, day)
    sow = dow * 86400 + hour * 3600 + min * 60 + sec
    return week, sow

# 经纬度转化为xyz(参考RTKLIB)
def llh2xyz(lat, lon, h):
    RE_WGS84 = 6378137.0
    FE_WGS84 = 1.0/298.257223563
    lat = lat * pi / 180
    lon = lon * pi / 180
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


# 从pos文件中读取坐标结果，并以xyz坐标形式输出
def readpos(posfilepath):
    f = open(posfilepath, encoding='gb18030', errors='ignore')
    ln = f.readline()
    posmode = 'xyz'
    while ln:
        if '%  GPST' in ln:
            if 'x-ecef(m)' in ln:
                posmode = 'xyz'
            elif 'latitude(deg)' in ln:
                posmode = 'llh'
            break
        ln = f.readline()
    xyz = []
    while ln:
        ln = f.readline()
        if not ln:
            break
        #content = ln.split(' ')
        if posmode == 'xyz':
            x = float(ln[24:38])
            y = float(ln[39:53])
            z = float(ln[54:69])
            xyz.append([x, y, z])
        elif posmode == 'llh':
            lat = float(ln[24:38])
            lon = float(ln[38:53])
            h = float(ln[53:64])
            xyz.append(llh2xyz(lat, lon, h))
    f.close()
    return xyz


# 根据测站id在snx文件中查找测站精确坐标
def getcrd(siteid, snxfilepath, xyz):
    snxcrd = []
    if snxfilepath == '':
        print('[WARNING] Not find the snxfile, use the average pos as substitute')
    else:
        f = open(snxfilepath, encoding='gb18030', errors='ignore')
        ln = f.readline()
        while ln:
            ln = f.readline()
            if not ln:
                print('[WARNING] Not find the siteid', siteid, ', use the average pos as substitute')
                break
            if ln[14:18] == siteid:
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                ln = f.readline()
                snxcrd.append(float(ln[47:68]))
                break
        f.close()
    if not snxcrd:
        x = 0
        y = 0
        z = 0
        for i in range(len(xyz)):
            x = x + xyz[i][0]
            y = y + xyz[i][1]
            z = z + xyz[i][2]
        snxcrd = [x/len(xyz), y/len(xyz), z/len(xyz)]
    else:
        print('[INFO] Find the sitecrd in the snx file')
    print('[INFO] The sitecrd is', snxcrd)
    return snxcrd


# xyz转换为llh（经纬度）
def xyz2llh(ecef):
    aell = 6378137
    fell = 1 / 298.257223563
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
    llh = [lat, long, h]
    return llh


# xyz转换至以测站精确坐标为基准的enu坐标
def xyz2enu(xyz, snxcrd):
    enu = []
    llhcrd = xyz2llh(snxcrd)
    phi = llhcrd[0]
    lam = llhcrd[1]
    sinphi = sin(phi)
    cosphi = cos(phi)
    sinlam = sin(lam)
    coslam = cos(lam)
    for i in range(len(xyz)):
        difxyz = [xyz[i][0]-snxcrd[0], xyz[i][1]-snxcrd[1], xyz[i][2]-snxcrd[2]]
        e = -sinlam*difxyz[0]+coslam*difxyz[1]
        n = -sinphi*coslam*difxyz[0]-sinphi*sinlam*difxyz[1]+cosphi*difxyz[2]
        u =  cosphi*coslam*difxyz[0]+cosphi*sinlam*difxyz[1]+sinphi*difxyz[2]
        enu.append([e, n, u])
    return enu

# 保存enu误差结果为CSV文件
def saveenu(enu, posfilepath):
    f = open(posfilepath[:-4] + '.csv', 'a', newline="")
    csv_write = csv.writer(f)
    for i in range(len(enu)):
        csv_write.writerow([enu[i][0], enu[i][1], enu[i][2]])
    f.close()
    return 0


# 绘制enu误差时间序列图
def plotenu(enu, con_time, posfilepath):
    e = []
    n = []
    u = []
    for i in range(len(enu)):
        e.append(enu[i][0])
        n.append(enu[i][1])
        u.append(enu[i][2])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.axis([0, len(enu)+1, -1, 1])
    ax.plot(range(1, len(enu)+1), e)
    ax.plot(range(1, len(enu)+1), n)
    ax.plot(range(1, len(enu)+1), u)
    ax.grid(True, linestyle='--')
    plt.xlabel('[Epoch]')
    plt.ylabel('[Error]')
    plt.legend(['E', 'N', 'U'])
    plt.text(1000, -0.65,'E: '+ str(con_time[0])+'min', fontsize=12)
    plt.text(1000, -0.75,'N: '+ str(con_time[1])+'min', fontsize=12)
    plt.text(1000, -0.85,'U: '+ str(con_time[2])+'min', fontsize=12)
    # plt.show()
    plt.savefig(posfilepath[:-4] + '.png', dpi=400)
    plt.close()
    return 0

# 收敛时间统计
def count(enu):
    con_time = [0, 0, 0]
    for j in range(3):
        for i in range(len(enu)-10):
            if abs(enu[i][j]) < 0.1 and abs(enu[i+1][j]) < 0.1 and abs(enu[i+2][j]) < 0.1 and abs(enu[i+3][j]) < 0.1 \
                    and abs(enu[i+4][j]) < 0.1 and abs(enu[i+5][j]) < 0.1 and abs(enu[i+6][j]) < 0.1 and \
                    abs(enu[i+7][j]) < 0.1 and abs(enu[i+8][j]) < 0.1 and abs(enu[i+9][j]) < 0.1 :
                con_time[j] = i/2
                break
    print(con_time)
    return con_time

def read_NetDiff_pos(file):
    xyzlist = []
    f = open(file)
    ln = f.readline()
    while ln:
        if ln[0] != '%':
            x = float(ln[76:88])
            y = float(ln[91:103])
            z = float(ln[106:118])
            year = int(ln[0:4])
            mouth = int(ln[5:7])
            day = int(ln[8:10])
            hour = int(ln[11:13])
            mini = int(ln[14:16])
            sec = int(ln[17:19])
            week, t = ymdhms2wksow(year, mouth, day, hour, mini, sec)
            xyzlist.append([x, y, z, t])
        ln = f.readline()
    print("[INFO] Finish Reading the Net_Diff pos file")
    return xyzlist


if __name__ == '__main__':

    # 此处修改文件路径
    posfilepath = r'C:\Users\LZ\Desktop\other work\Liu WenXuan\21770\Coor_2021269_ABPO-ABPO.pos'
    snxfilepath = r'C:\Users\LZ\Desktop\other work\Liu WenXuan\21770\igs2177.snx'

    siteid = posfilepath[-8:-4].upper()
    print('[INFO] The siteid is :', siteid)
    # xyz = readpos(posfilepath)
    xyz = read_NetDiff_pos(posfilepath)
    snxcrd = getcrd(siteid, snxfilepath, xyz)
    enu = xyz2enu(xyz, snxcrd)
    con_time = count(enu)
    # saveenu(enu, posfilepath)
    plotenu(enu, con_time, posfilepath)
