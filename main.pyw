import os
import sys
import tkinter.messagebox, tkinter.filedialog
from tkinter import *


def search(path):
    try:
        # 整理格式
        if not path[-1] == '\\' and not path[-1] == '/':
            path += '\\'
    except IndexError:
        tkinter.messagebox.askokcancel("错误：路径栏为空", "请输入路径")
        return
    path = path.replace("/", "\\")
    empty_folder = [] # 空文件夹列表
    empty_file = [] # 空文件列表
    subfolder = [] # 子文件夹列表
    subfile = [] # 文件列表
    Exclusion_list = ["System Volume Information", "Config.Msi", "WindowsApps", "Documents and Settings"] # 排除列表
    try:
        for file in os.listdir(path): # 获取所有子文件夹 & 文件
            if os.path.isdir(path + file) and file not in Exclusion_list:
                subfolder.append(path + file)
            elif os.path.isfile(path + file) and file not in Exclusion_list:
                subfile.append(path + file)
    except PermissionError:
        tkinter.messagebox.askokcancel("错误：在寻找子文件夹时拒绝访问", sys.exc_info()[1] + '\n已记录的子文件夹：' + str(subfolder))
    except FileNotFoundError:
        tkinter.messagebox.askokcancel("错误：系统找不到指定的路径", sys.exc_info()[1])
    except OSError:
        tkinter.messagebox.askokcancel("错误：OS模块错误", sys.exc_info()[1])
    try:
        for file in subfolder:
            if not os.listdir(file): # 检测空文件夹
                empty_folder.append("Folder#" + file)
        for file in subfile:
            if os.path.getsize(file) == 0: # 检测空文件
                empty_file.append("File#" + file)
    except PermissionError:
        tkinter.messagebox.askokcancel("错误：在寻找空文件夹时拒绝访问", str(sys.exc_info()[1]) + '\n已记录的空文件夹：' + str(empty_folder))
    return empty_folder + empty_file

def ShowEmptyFolder():
    Path = FoldPath.get()
    Fold.delete(0, END)
    for p in search(Path):
        Fold.insert(END, p) # 显示

def DelFold():
    if Fold.size() != 0:
        FoldList = Fold.get(Fold.curselection()).split("#")
        DelFoldPath = FoldList[1]
        FoldIndex = Fold.curselection()
        if FoldIndex != ():
            DelFold = Fold.get(FoldIndex)
            if FoldList[0] == 'Folder':
                os.rmdir(DelFoldPath)
                Fold.delete(FoldIndex)
            elif FoldList[0] == 'File':
                os.remove(DelFoldPath)
                Fold.delete(FoldIndex)

def DelAll():
    DelFoldList = Fold.get(0, END)
    for DelFold in DelFoldList:
        if DelFold.split("#")[0] == 'Folder':
            os.rmdir(DelFold.split("#")[1])
        elif DelFold.split("#")[0] == 'File':
            os.remove(DelFold.split("#")[1])
    Fold.delete(0, END)
def DelAllFold():
    n = 0
    while n <= Fold.size():
        if Fold.get(n).split("#")[0] == 'Folder':
            os.rmdir(Fold.get(n).split("#")[1])
            Fold.delete(n)
            n -= 1
        n += 1
def DelAllFile():
    n = 0
    while n <= Fold.size():
        if Fold.get(n).split("#")[0] == 'File':
            os.remove(Fold.get(n).split("#")[1])
            Fold.delete(n)
            n -= 1
        n += 1


def DiaFolder():
    filenames = tkinter.filedialog.askdirectory()
    FoldPath.delete(0, END)
    FoldPath.insert(END, filenames)
    ShowEmptyFolder()

root = Tk()
root.minsize(340, 450)
root.geometry("360x480")
root.title("删除空文件夹 & 空文件")

FoldPath = Entry(root)
FoldPath.place(relx=0.05, rely=0.005, relwidth=0.61, relheight=0.04) # 文件夹地址输入框
FoldDia = Button(root, text="选择文件", command=DiaFolder)
FoldDia.place(relx=0.67, rely=0.005, relwidth=0.15, relheight=0.04)
Sure = Button(root, text="确定", command=ShowEmptyFolder)
Sure.place(relx=0.82, rely=0.005, relwidth=0.13, relheight=0.04)

Fold = Listbox(root) # 空文件夹显示框
Fold.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.88)
Del = Button(root, text='删除', command=DelFold) # 删除
Del.place(relx=0.05,rely=0.94,relwidth=0.2, relheight=0.05)
DelAll = Button(root, text='删除全部', command=DelAll) # 删除全部
DelAll.place(relx=0.75,rely=0.94,relwidth=0.2, relheight=0.05)
DelAllFold = Button(root, text='删除全部文件夹', command=DelAllFold) # 删除全部文件夹
DelAllFold.place(relx=0.50,rely=0.94,relwidth=0.25, relheight=0.05)
DelAllFile = Button(root, text='删除全部文件', command=DelAllFile) # 删除全部文件
DelAllFile.place(relx=0.27,rely=0.94,relwidth=0.23, relheight=0.05)

root.mainloop()