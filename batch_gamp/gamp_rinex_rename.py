# rinex_rename.py
# Author:LZ-CUMT
# Rename RINXE file from long to short by Batch processing
# Change File Name to GAMP File Name Format

# Choose the file path where you want to rename the rinex files
# obs  filename : ABMF00GLP_R_20200010000_01D_30S_MO.cro   ==> abmf0010.20o
# obs  filename : ABMF00GLP_R_20200010000_01D_30S_MO.crx   ==> abmf0010.20o
# nav  filename : BRDC00IGS_R_20200010000_01D_MN.rnx       ==> brdm0010.20p
# sp3  filename : GFZ0MGXRAP_20200010000_01D_05M_ORB.SP3   ==> gfz20863.sp3
# clk  filename : GFZ0MGXRAP_20200010000_01D_30S_CLK.CLK   ==> gfz20863.clk
# bia  filename : GBM0MGXRAP_20200010000_01D_30S_ABS.BIA   ==> gbm20863.bia
# p2c2 filename : P2C22001_RINEX.DCB                       ==> P2C22001.DCB
# erp  filename : igs20P2086.erp                           ==> igs20867.erp
# snx  filename : igs20P2086.snx                           ==>  igs2086.snx
#


import os
import math
from tkinter import filedialog

#     Change year,month,day to Modified Julian Day
def ymd2mjd(year, mon, day):
    if mon <= 2:
        mon += 12
        year -= 1
    mjd = 365.25 * year - 365.25 * year % 1.0 - 679006.0
    mjd += math.floor(30.6001 * (mon + 1)) + 2.0 - math.floor(
        year / 100.0) + math.floor(year / 400) + day
    return mjd

#      Change year, day of year to GPS week, day of week
def yrdoy2gpst(year, doy):
    date_1980jan6 = ymd2mjd(1980, 1, 6)
    date = ymd2mjd(year, 1, 1)
    time_delta = date - date_1980jan6
    days_delta = time_delta + doy - 1
    gps_week = int(days_delta/7)
    gps_dow = int(days_delta - gps_week*7)
    return gps_week, gps_dow

def renamefile(path, file, renamef):
    if os.path.isfile(os.path.join(path, renamef)):
        print("The file", renamef, "has already existed!")
    else:
        os.rename(os.path.join(path, file), os.path.join(path, renamef))

def main():
    path = filedialog.askdirectory()
    CRX2RNX_EXE = f"{path}/crx2rnx.exe"

    for file in os.listdir(path):
        if file[-4:] == ".cro":
            obsrename = (file[0:4]).lower()+file[16:19]+"0."+file[14:16]+"o"
            renamefile(path, file, obsrename)
        elif file[-4:] == ".crx":
            print(f"{file}")
            os.system(f"{CRX2RNX_EXE} -d {path}/{file}")
            os.remove(f"{path}/{file}")
            rnxfile = file[:-3]+'rnx'
            obsrename = (file[0:4]).lower()+file[16:19]+"0."+file[14:16]+"o"
            renamefile(path, rnxfile, obsrename)
        elif file[-4:] == ".rnx":
            if file[0:4] == "BRDC":
                navrename = "brdm"+file[16:19]+"0."+file[14:16]+"p"
            else:
                navrename = (file[0:4]).lower()+file[16:19]+"0."+file[14:16]+"p"
            renamefile(path, file, navrename)
        elif file[-4:] == ".SP3":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            sp3rename = (file[0:3]).lower()+str(week)+str(dow)+".sp3"
            renamefile(path, file, sp3rename)
        elif file[-4:] == ".CLK":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            clkrename = (file[0:3]).lower()+str(week)+str(dow)+".clk"
            renamefile(path, file, clkrename)
        elif file[-4:] == ".BIA":
            year = int(file[11:15])
            doy = int(file[15:18])
            week, dow = yrdoy2gpst(year, doy)
            biarename = (file[0:3]).lower()+str(week)+str(dow)+".bia"
            renamefile(path, file, biarename)
        elif file[-9:] == "RINEX.DCB":
            p2c2rename = file[0:8]+file[-4:]
            renamefile(path, file, p2c2rename)
        elif file[-4:] == ".erp":
            if file[5] == "P":
                erprename = file[0:3]+file[6:10]+'7'+file[-4:]
                renamefile(path, file, erprename)
        elif file[-4:] == ".snx":
            if file[5] == "P":
                snxrename = file[0:3]+file[-8:]
                renamefile(path, file, snxrename)

    print(" Exchange Complete! ")


if __name__ == "__main__":
    main()
