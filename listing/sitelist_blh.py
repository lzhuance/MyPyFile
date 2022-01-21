#!/usr/bin/python
# coding=utf-8

"""
根据站点列表文件site.list获取站点坐标详细信息
Version：1.0
Author:LZ_CUMT
"""

from gnss_cmn.crd_conv import xyz2llh


# 根据测站id在snx文件中查找测站精确坐标
def getcrd(siteid, snxfilepath):
    snxcrd = []
    if snxfilepath == '':
        print('[WARNING] Not find the snxfile, use the average pos as substitute')
    else:
        f = open(snxfilepath, encoding='gb18030', errors='ignore')
        line = f.readline()
        while line:
            line = f.readline()
            if not line:
                print('[WARNING] Not find the siteid', siteid, ', use the average pos as substitute')
                break
            if line[14:18] == siteid:
                snxcrd.append(float(line[47:68]))
                line = f.readline()
                snxcrd.append(float(line[47:68]))
                line = f.readline()
                snxcrd.append(float(line[47:68]))
                break
        f.close()
    return snxcrd


if __name__ == '__main__':
    filepath = "C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\site1.list"
    snxfilepath = "C:\\Users\\LZ\\Desktop\\gnss_input\\igs21P2170.snx"
    writepath = "C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\sitesnx11.list"
    writepath2 = "C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\site11.list"
    f = open(filepath, encoding='gb18030', errors='ignore')
    fw = open(writepath, "w")
    fw2 = open(writepath2, "w")
    ln = f.readline()

    while ln:
        siteid = ln[0:4]
        snxcrd = getcrd(siteid.upper(), snxfilepath)
        if snxcrd:
            snxllh = xyz2llh(snxcrd)
            output = "{}  {:16.7f}  {:16.7f}  {:16.7f}  {:14.7f}  {:14.7f}  {:14.7f}\n"\
                .format(siteid, snxcrd[0], snxcrd[1], snxcrd[2], snxllh[0], snxllh[1], snxllh[2])
            fw.write(output)
            fw2.write(siteid)
            fw2.write("\n")
        ln = f.readline()
        if not ln:
            break
