#created by LZ_CUMT

import os
from tkinter import filedialog

def renamefile(path,file,renamef):
    if os.path.isfile(os.path.join(path, renamef)):
        print("The file",renamef,"has already existed!")
    else:
        os.rename(os.path.join(path, file), os.path.join(path, renamef))

def main():
    path = filedialog.askdirectory()
    for file in os.listdir(path):
        if file[-6:]==".ifamb":
            obsrename=(file[0:4]).upper()+"_ambupd_20"+file[9:11]+file[4:7]
            renamefile(path, file, obsrename)
    print(" Exchange Complete! ")

if __name__ == "__main__":
    main()