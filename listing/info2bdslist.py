#!/usr/bin/python
# coding=utf-8


if __name__ == '__main__':
    filepath = 'C:\\Users\\LZ\\Desktop\\siteinfo.txt'
    writepath = 'C:\\Users\\LZ\\Desktop\\bdssite.list'
    f = open(filepath, encoding='gb18030', errors='ignore')
    fw = open(writepath, "w")
    ln = f.readline()
    while ln:
        ln = f.readline()
        bdnumtype=int(ln[30:33])
        if bdnumtype>=15:
            fw.write(ln[0:4])
            fw.write('\n')
        if not ln:
            break