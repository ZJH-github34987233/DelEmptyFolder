from tkinter import *
import os

def search(path):
    if path[-1] == '\\' or path[-1] == '/':
        path = path[0:-1]
    path = path.replace("/", "\\")
    empty_folder = []
    files = os.listdir(path)  # 获取路径下的子文件(夹)列表
    for file in files:
        file_dir = path + '\\' + file
        if os.path.isdir(file_dir):  # 如果是文件夹
            if not os.listdir(file_dir):  # 如果子文件为空
                empty_folder.append(file_dir)
        # elif os.path.isfile(file):  # 如果是文件
        #     if os.path.getsize(file) == 0:  # 文件大小为0
        #         empty_folder.append(path + "\\" + file)
    return empty_folder

def ShowEmptyFolder():
    Path = FoldPath.get()
    Fold.delete(0, END)
    for p in search(Path):
        Fold.insert(END, p) # 显示

def DelFold():
    DelFoldindex = Fold.curselection()
    if DelFoldindex != ():
        DelFold = Fold.get(DelFoldindex)
        os.rmdir(DelFold)
        Fold.delete(DelFoldindex)

def DelAllFold():
    DelFoldList = Fold.get(0, END)
    for DelFold in DelFoldList:
        os.rmdir(DelFold)
    Fold.delete(0, END)

root = Tk()
root.minsize(360, 480)
root.geometry("360x480")
root.title("删除空文件夹")

FoldPath = Entry(root)
FoldPath.place(relx=0.05, rely=0.005, relwidth=0.75, relheight=0.04) # 文件夹地址输入框
Sure = Button(root, text="确定", command=ShowEmptyFolder)
Sure.place(relx=0.82, rely=0.005, relwidth=0.13, relheight=0.04)

Fold = Listbox(root) # 空文件夹显示框
Fold.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.88)
Del = Button(root, text='删除', command=DelFold) # 删除
Del.place(relx=0.05,rely=0.94,relwidth=0.2, relheight=0.05)
DelAll = Button(root, text='删除全部', command=DelAllFold) # 删除全部
DelAll.place(relx=0.75,rely=0.94,relwidth=0.2, relheight=0.05)

root.mainloop()