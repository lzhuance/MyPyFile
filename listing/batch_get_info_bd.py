#!/usr/bin/python
# coding=utf-8
"""
遍历当前文件下所有o文件，读取头文件信息并存储含北斗新信号的测站信息至bdssite.info，
存储详细观测值信息至bdssitetype.info
bdssitetype.info:
1   abpo   18   SEPT POLARX5         C1P L1P S1P C5P L5P S5P C2I L2I S2I C7I L7I S7I C6I L6I S6I C7D L7D S7D
2   aggo   20   SEPT POLARX5TR       C1P L1P D1P S1P C5P L5P D5P S5P C2I L2I D2I S2I C7I L7I D7I S7I C6I L6I D6I S6I
3   amc4   18   SEPT POLARX5TR       C1P L1P S1P C5P L5P S5P C2I L2I S2I C7I L7I S7I C6I L6I S6I C7D L7D S7D
4   areg   24   SEPT POLARX5         C1P L1P D1P S1P C5P L5P D5P S5P C2I L2I D2I S2I C7I L7I D7I S7I C6I L6I D6I S6I C7D L7D D7D S7D
......

bdssite.list:
abpo
aggo
amc4
areg
arht
......

"""

import os



if __name__ == '__main__':
    filepath="D:\\paperdata\\2021\\183\\daily"
    writepath = 'C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\bdssitetype.info'
    wlistpath = 'C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\bdssite.list'
    fw = open(writepath,"w")
    fl= open(wlistpath, "w")
    index = 0
    for file in os.listdir(filepath):
        f = open(filepath+"\\"+file,encoding='gb18030', errors='ignore')
        ln = f.readline()
        cnum = 0

        while ln:
            if 'RINEX VERSION / TYPE' in ln:
                ver = float(ln[5:9])
            if 'SYS / # / OBS TYPES' in ln:
                if ln[0]=='C':
                    cnum=int(ln[4:6])
                    if cnum > 13:
                        ln1=f.readline()
                        ctype=ln[7:59]+ln1[7:59]
                    elif cnum > 26:
                        ln1=f.readline()
                        ln2=f.readline()
                        ctype=ln[7:59]+ln1[7:59]+ln2[7:59]
            if 'REC # / TYPE / VERS' in ln:
                rec = ln[20:40]
            if 'END OF HEADER' in ln:
                break
            ln = f.readline()
        f.close

        if cnum > 13:
            index += 1
            output="{:3d}   {}{:5d}   {} {}\n".format(index,file[0:4],cnum,rec,ctype)
            fw.write(output)
            fl.write(file[0:4])
            fl.write('\n')