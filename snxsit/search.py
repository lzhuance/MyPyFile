
sscfile='ADIS505_20201203_CGIRAW_100HZ.csv'
newfile='ADIS505_20201203_CGIRAW_100HZ_New.csv'
f = open(sscfile)
f1 = open(newfile,'a+')
ln = f.readline()
while ln:
    ln = f.readline()
    if not ln:
        break
    if ln[0:3] == "IMU":
        f1.write(ln)