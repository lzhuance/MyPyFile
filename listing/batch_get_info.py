#!/usr/bin/python
# coding=utf-8
import os
'''
遍历当前文件下所有o文件，读取头文件信息并存储至site.info
Version：1.0
Author:LZ_CUMT

site.info:
site     ver    G    R    E    C    J    I    S   RecType
abmf    3.04   18   20   20   12   12    4    8   SEPT POLARX5        
abpo    3.04   17   12   15   18   15    0    0   SEPT POLARX5        
acrg    3.04   24   16    8    0    0    0    0   JAVAD TR_G3TH       
aggo    3.04   22   20   20   20    0    4    8   SEPT POLARX5TR      
......
'''


if __name__ == '__main__':
    filepath="D:\\paperdata\\2021\\182\\daily"
    writepath = 'C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\site.info'
    fw = open(writepath,"w")
    fw.write('site     ver    G    R    E    C    J    I    S   RecType\n')
    for file in os.listdir(filepath):
        f = open(filepath+"\\"+file,encoding='gb18030', errors='ignore')
        ln = f.readline()
        gnum = 0
        rnum = 0
        enum = 0
        cnum = 0
        jnum = 0
        inum = 0
        snum = 0
        while ln:
            if 'RINEX VERSION / TYPE' in ln:
                ver = float(ln[5:9])
            if 'SYS / # / OBS TYPES' in ln:
                if ln[0]=='G':
                    gnum=int(ln[4:6])
                elif ln[0]=='R':
                    rnum=int(ln[4:6])
                elif ln[0]=='E':
                    enum=int(ln[4:6])
                elif ln[0]=='C':
                    cnum=int(ln[4:6])
                elif ln[0]=='J':
                    jnum=int(ln[4:6])
                elif ln[0]=='I':
                    inum=int(ln[4:6])
                elif ln[0]=='S':
                    snum=int(ln[4:6])
            if 'REC # / TYPE / VERS' in ln:
                rec = ln[20:40]
            if 'END OF HEADER' in ln:
                break
            ln = f.readline()
        f.close
        output="{}{:8.2f}{:5d}{:5d}{:5d}{:5d}{:5d}{:5d}{:5d}   {}\n".format(file[0:4],ver,gnum,rnum,enum,cnum,jnum,inum,snum,rec)
        fw.write(output)