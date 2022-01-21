#!/usr/bin/python
# coding=utf-8

'''
根据wget导出的.listing列表获取测站列表文件site.list用于gamp_good下载
Version：1.0
Author:LZ_CUMT
'''
if __name__ == '__main__':
    filepath = 'C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\.listing'
    writepath = 'C:\\Users\\LZ\\Desktop\\BDS_SITE_INFO\\site_gps.list'
    f = open(filepath,encoding='gb18030', errors='ignore')
    fw = open(writepath,"w")
    ln = f.readline()
    while ln:
        if len(ln)==98:
            str=ln[56:60].lower()
            fw.write(str)
            fw.write("\n")
        ln = f.readline()
        if not ln:
            break
    f.close
