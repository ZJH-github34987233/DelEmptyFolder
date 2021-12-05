#!/usr/bin/python
# -*- coding: UTF-8 -*-

try:
    import json
    import logging
    import os
    import sys
    import time
    import tkinter.filedialog
    import tkinter.messagebox
    import traceback
    from tkinter import *

    def ReadSettings():
        global LOG_FORMAT
        ## ==== 默认值 ==== ##
        LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(process)d] %(message)s" # 格式默认值
        ## ==== 默认值 ==== ##
        if not os.path.exists("DEF/set.json"):  # 检测是否有set
            return False
        with open("DEF/set.json", "r") as S:
            log_format = json.load(S).get("Format")
            if log_format:
                LOG_FORMAT = log_format # 日志格式

    ReadSettings()

    ## ==== 日志初始化 ==== ##
    os.makedirs("DEF/Log", exist_ok = True)
    File = os.listdir("DEF/Log") # 获取所有日志文件
    count_log = 5 # 日志个数
    while len(File) > 0:
        count_log = 9 if count_log > 9 else count_log # 限制个数
        file = File.pop() # 获取文件路径
        filename = file.split(".")[0] # 获取文件名
        num = int(filename.split("Log")[1]) # 获取日志编号
        os.rename(f"DEF/Log/{file}", f"DEF/Log/Log{num+1}.log") # 重命名
        if num >= count_log: # 清理日志文件
            os.remove(f"DEF/Log/Log{num+1}.log")

    logging.basicConfig(filename=f'DEF/Log/Log1.log', format=LOG_FORMAT, level=logging.INFO, encoding='utf-8') # 日志设置
    ## ==== 日志初始化 ==== ##
    def Reboot(): # 重启应用
        logging.info("[重启应用] 尝试重启应用")
        root.destroy()
        logging.info("[重启应用] 应用已关闭")
        if os.path.exists("main.pyw"):
            os.startfile("main.pyw")
        elif os.path.exists("main.exe"):
            os.startfile("main.exe")
        logging.info("[重启应用] 应用已重新启动\n")

    def ChooseFilePath():
        logging.info("[文件选择] 文件选择窗口已开启")
        Path = tkinter.filedialog.askdirectory()
        logging.info("[文件选择] 已选择 " + Path)
        return Path

    def message(title, message, value=0):
        match value: # 日志记录
            case 0:
                choose = tkinter.messagebox.showinfo(title, message)  # 输出
                logging.info(f"[未知弹窗] 弹窗已开启")
                logging.info("[未知弹窗] 弹窗内容：\n" + "[标题] " + str(title) + '\n' + "[内容] " + str(message))
            case 1:
                choose = tkinter.messagebox.showinfo(title, message)  # 输出
                logging.info(f"[普通弹窗 - {title}] 弹窗已开启")
                logging.debug(f"[普通弹窗 - {title}] 弹窗内容：\n" + "[标题] " + str(title) + '\n' + "[内容] " + str(message))
            case 2:
                choose = tkinter.messagebox.showwarning(title, message)  # 输出
                logging.error(f"[异常弹窗] 弹窗已开启")
                logging.error("[异常弹窗] 弹窗内容：\n" + "[标题] " + str(title) + '\n' + "[内容] " + str(message))
            case 3:
                choose = tkinter.messagebox.showerror(title, message)  # 输出
                logging.error(f"[错误弹窗] 弹窗已开启")
                logging.error("[错误弹窗] 弹窗内容：\n" + "[标题] " + str(title) + '\n' + "[内容] " + str(message))
                logging.exception("报错内容如下")
            case 4:
                choose = tkinter.messagebox.askokcancel(title, message) # 输出
                logging.info(f"[对话框 - {title}] 弹窗已开启")
                logging.debug(f"[对话框 - {title}] 弹窗内容：\n" + "[标题] " + str(title) + '\n' + "[内容] " + str(message))
                logging.info(f"[对话框 - {title}] 用户选择了确定") if choose else logging.info(f"[对话框 - {title}] 用户选择了取消")
                return choose
            case _:
                choose = tkinter.messagebox.showinfo(title, message)  # 输出

    def Tolist(string:str):
        logging.info("[字符串转列表] 字符串转列表函数被调用")
        if not '[' in string or not ']' in string:
            logging.info(f"[字符串转列表] 字符串 {string} 不是列表格式")
            return string
        string = string.replace("[", "").replace("]", ""). replace("(", "").replace(")", "") # 获取元素
        logging.info(f"[字符串转列表] 字符串中包含的元素有 {string}")
        list = string.split(",")
        logging.info(f"[字符串转列表] 已将字符串初步转化为列表，列表如下：\n{list}")
        logging.info(f"[字符串转列表] 开始整理列表")
        FinallyList = []
        for i in list:
            try:
                FinallyList.append(int(i))
                logging.info(f"[字符串转列表] 已将 {i} 转化为 int 类型")
            except:
                if i[0] == ' ':
                    FinallyList.append(i.replace("'", "")[1:])
                else:
                    FinallyList.append(i.replace("'", ""))
        logging.info(f"[字符串转列表] 已将字符串完全转化为列表，列表如下：\n{FinallyList}\n它的类型为：{type(FinallyList)}")
        return FinallyList

    def WorkExp(Exp):
        logging.info("[拓展组件] 开始运行拓展组件")
        os_str = f'python {Exp}'
        f = os.popen(os_str, 'r')
        logging.info("[拓展组件] 组件已开启")
        res = f.readlines()  # res接受返回结果
        logging.info(f"[拓展组件] 已接收到组件输出结果为 {res}（未处理）")
        logging.info(f"[拓展组件] 开始处理输出结果")
        exp_print = []
        for i in res:
            exp_print.append(Tolist(i.encode("gbk").decode().replace("\n", "")))
        logging.info(f"[拓展组件] 已将结果处理为 {exp_print}")
        logging.info(f"[拓展组件] 正在执行输出")
        for i in exp_print:
            if type(i) == type(["列表"]):
                match i[0]:
                    case "|Append|":
                            for c in i[2:]:
                                exec(f"{i[1]}.insert(END, c)")
                    case "|Replace|":
                        exec(f"{i[1]}.delete(0, END)")
                        for c in i[2:]:
                            exec(f"{i[1]}.insert(END, c)")
                    case "|Variable|":
                        exec(f"global {i[1]}")
                        if i[2] != "|Empty|":
                            exec(f"{i[1]} = {i[2]}")
                        else:
                            exec(f"{i[1]} = ''")
        logging.info(f"[拓展组件] 输出已执行完毕")
        Connect = ''
        for i in exp_print: # 显示输出内容
            Connect += str(i) + '\t'
        message("组件输出", f"组件输出了以下内容\n{Connect}", 1)
        f.close()

    def ExpansionComponents(): # 拓展组件
        IsEXC = message("拓展组件正在测试", "目前拓展组件尚在测试中，是否检测及使用拓展组件", 4)
        if not IsEXC:
            return

        os.makedirs("DEF/ExpansionComponents", exist_ok=True) # 创建文件夹
        exp_file = os.listdir("DEF/ExpansionComponents") # 检测文件
        LenExp = len(exp_file)
        count = 0
        n = 0
        c = 1
        while count < LenExp:
            if os.path.isdir("DEF/ExpansionComponents/" + str(exp_file[count])):
                Old = "DEF/ExpansionComponents/" + str(exp_file[count])
                exp_file.append([Old] + os.listdir("DEF/ExpansionComponents/" + str(exp_file[count])));del exp_file[count] # 替换
                LenExp = len(exp_file) # 更新数据
                logging.info("[拓展组件] 检测到文件夹 " + Old)
            else:
                count += 1
        while n < len(exp_file):
            c = 1
            if type(exp_file[n]) == type([]):
                while c < len(exp_file[n]):
                    if os.path.isdir(exp_file[n][0] + "/" + exp_file[n][c]):
                        del exp_file[n][c]
                    else:
                        c += 1
            n += 1
        if exp_file:
            logging.info("[拓展组件] 检测到以下组件：\n" + str(exp_file))
        else:
            return
        logging.info("[拓展组件] 开始运行组件")
        menuExp = Menu(mainmenu, tearoff=0)  # 菜单分组 menuExp
        mainmenu.add_cascade(label="拓展组件", menu=menuExp)
        # 运行组件
        for i in exp_file:
            if list(i) == i:
                file = i[1:]
                fold = i[0]
                logging.info('[拓展组件] ' + str(file) + f"是 {fold} 文件夹中的文件")
                for f in file:
                    Exp = fold + '/' + str(f)
                    try:
                        exec(f'menuExp.add_command(label="{f.split(".")[0]}", command=lambda:WorkExp("{Exp}"))')
                    except AttributeError:
                        logging.error("[拓展组件] 组件加载失败 {Exp} 组件中没有init函数")
                    except SyntaxError:
                        logging.error("[拓展组件] 组件命名不规范，请更改或删除 {Exp} 中的特殊符号")

            else:
                logging.info('[拓展组件] ' + i + "不是文件夹")
                Exp = 'DEF/ExpansionComponents/' + str(i)
                try:
                    exec(f'menuExp.add_command(label="{i.replace(".py", "")}", command=lambda:WorkExp("{Exp}"))')
                except AttributeError:
                    message("错误：语法错误", str(sys.exc_info()[1]), 3)

    def search(path): # 空文件列表
        logging.info("[获取空文件] 获取空文件函数被调用")
        try:
            # 整理格式
            if not path[-1] == '\\' and not path[-1] == '/':
                path += '\\'
                logging.info("[获取空文件] 已成功整理格式")
        except IndexError:
            message("错误：路径栏为空！", "请输入路径", 2)
            return
        path = path.replace("/", "\\")
        empty_folder = [] # 空文件夹列表
        empty_file = [] # 空文件列表
        subfolder = [] # 子文件夹列表
        subfile = [] # 文件列表
        try:
            logging.info("[获取空文件] 开始获取子文件")
            for file in os.listdir(path): # 获取所有子文件夹 & 文件
                try:
                    if os.path.isdir(path + file):
                        subfolder.append(path + file)
                    elif os.path.isfile(path + file):
                        subfile.append(path + file)
                except PermissionError:
                    message("错误：在寻找子文件夹时拒绝访问", str(sys.exc_info()[1]) + '\n已记录的子文件夹：' + str(subfolder), 3)
            logging.info("[获取空文件] 获取子文件完成")
        except FileNotFoundError:
            message("错误：系统找不到指定的路径", str(sys.exc_info()[1]), 3)
            FoldPath.delete(0, END)
        except OSError:
            message("错误：OS模块错误", str(sys.exc_info()[1]), 3)

        logging.info("[获取空文件] 开始检测空文件夹")
        for file in subfolder:
            try:
                if not os.listdir(file): # 检测空文件夹
                    empty_folder.append(file)
                    logging.debug("[获取空文件] 检测到空文件夹 " + file)
            except PermissionError:
                continue
        logging.info("[获取空文件] 检测空文件夹完成，共检测到 " + str(len(empty_folder)) + " 个空文件夹")
        logging.info("[获取空文件] 开始检测空文件")
        for file in subfile:
            try:
                if os.path.getsize(file) == 0: # 检测空文件
                    empty_file.append(file)
                    logging.debug("[获取空文件] 检测到空文件 " + file)
            except PermissionError:
                continue
        logging.info("[获取空文件] 检测空文件完成，共检测到 " + str(len(empty_file)) + " 个空文件")
        logging.info("[获取空文件] 已获取所有空文件\n")
        return empty_folder + empty_file

    def ShowEmptyFolder():
        try:
            logging.info("[显示空文件列表] 显示空文件列表被调用")
            Path = FoldPath.get()
            logging.info("[显示空文件列表] 检测到路径为" + Path)
            Fold.delete(0, END)
            logging.info("[显示空文件列表] 成功删除原文件列表")
            logging.info("[显示空文件列表] 开始显示空文件列表")
            for p in search(Path):
                Fold.insert(END, p) # 显示
                logging.debug("[显示空文件列表] 已显示 " + p)
            logging.info("[显示空文件列表] 显示空文件列表完成，共显示了 " + str(Fold.size()) + " 个空文件\n")
        except:
            message(f"错误：{sys.exc_info()[0]}", str(sys.exc_info()[1]), 3)

    def DelFold():
        try:
            logging.info("[删除选中文件] 删除选中文件函数被调用")
            if Fold.size() != 0:
                logging.info("[删除选中文件] 正在获取选中文件相关信息")
                DelFoldPath = Fold.get(Fold.curselection())
                FoldIndex = Fold.curselection() # 选中的文件路径索引
                logging.info("[删除选中文件] 已获取选中文件相关信息")
                if FoldIndex != ():
                    logging.info("[删除选中文件] 正在删除选中文件")
                    if message("警告", "你是否要删除 " + DelFoldPath, 4):
                        match os.path.isdir(DelFoldPath):
                            case True:
                                logging.debug("[删除选中文件] 检测到 " + DelFoldPath + ' 是文件夹')
                                os.rmdir(DelFoldPath)
                                Fold.delete(FoldIndex) # 删除列表显示
                                logging.info("[删除选中文件] 已删除选中文件夹\n")
                            case False:
                                logging.debug("[删除选中文件] 检测到 " + DelFoldPath + ' 是文件')
                                os.remove(DelFoldPath)
                                Fold.delete(FoldIndex) # 删除列表显示
                                logging.info("[删除选中文件] 已删除选中文件\n")
        except FileNotFoundError:
            message("错误：系统找不到指定的路径", str(sys.exc_info()[1]), 3)
        except PermissionError:
            message("错误：在删除文件时拒绝访问", str(sys.exc_info()[1]), 3)

    def DelAll():
        logging.info("[删除所有文件和文件夹] 删除所有文件和文件夹函数被调用")
        if message("警告", "你是否要删除所有文件和文件夹", 4):
            logging.info("[删除所有文件和文件夹] 正在获取所有文件列表")
            DelFoldList = Fold.get(0, END)
            logging.info("[删除所有文件和文件夹] 已获取所有文件列表")
            for DelFold in DelFoldList:
                match os.path.isdir(DelFold):
                    case True:
                        logging.debug("[删除所有文件和文件夹] 检测到 " + DelFold + ' 是文件夹')
                        os.rmdir(DelFold)
                        logging.debug("[删除所有文件和文件夹] 已删除文件夹 " + DelFold)
                    case False:
                        logging.debug("[删除所有文件和文件夹] 检测到 " + DelFold + ' 是文件')
                        os.remove(DelFold)
                        logging.debug("[删除所有文件和文件夹] 已删除文件 " + DelFold)
            Fold.delete(0, END)
            logging.info("[删除所有文件和文件夹] 已删除所有文件和文件夹\n")
    def DelAllFold():
        logging.info("[删除所有文件夹] 删除所有文件夹函数被调用")
        if message("警告", "你是否要删除所有文件夹", 4):
            n = 0
            while n <= Fold.size():
                if os.path.isdir(Fold.get(n)):
                    logging.debug("[删除所有文件夹] 检测到 " + Fold.get(n) + ' 是文件夹')
                    os.rmdir(Fold.get(n))
                    logging.debug("[删除所有文件夹] 已删除文件夹 " + Fold.get(n))
                    Fold.delete(n) # 删除列表显示
                    n -= 1
                n += 1
            logging.info("[删除所有文件夹] 已删除所有文件夹\n")
    def DelAllFile():
        logging.info("[删除所有文件] 删除所有文件函数被调用")
        if message("警告", "你是否要删除所有文件", 4):
            n = 0
            while n <= Fold.size():
                try:
                    if os.path.isfile(Fold.get(n)):
                        logging.debug("[删除所有文件] 检测到 " + Fold.get(n) + ' 是文件')
                        os.remove(Fold.get(n))
                        logging.debug("[删除所有文件] 已删除文件 " + Fold.get(n))
                        Fold.delete(n) # 删除列表显示
                        n -= 1
                    n += 1
                except IndexError:
                    message("错误：索引超出范围", sys.exc_info()[1], 3)
            logging.info("[删除所有文件夹] 已删除所有文件\n")


    def DiaFolder():
        filenames = ChooseFilePath()
        if filenames:
            FoldPath.delete(0, END)
            FoldPath.insert(END, filenames)
            ShowEmptyFolder() # 显示

    def Setting():
        logging.info("[设置] 设置函数被调用")
        # 重置
        def Reset():
            if message("是否要重置", "重置设置后会使应用重启", 4):
                if os.path.exists("DEF/set.json"):
                    os.remove("DEF/set.json")
                LoggingFormatSetting.delete(0, END)
                LoggingFormatSetting.insert(END, LOG_FORMAT)
                Debug.deselect()
                Reboot()

        # 保存
        def Fix():
            logging.info("[设置] 正在保存设置")
            is_save = True
            is_reboot = True
            is_save_format = True
            ## ==== 数据储存 ==== ##
            # == 日志格式 == #
            if LoggingFormatSetting.get(): # 日志格式
                is_save_format = True
                Format = LoggingFormatSetting.get()
                logging.info("[设置 - 日志格式] 已成功获取用户输入的格式为 " + Format)
            else:
                message("提示：日志格式框内无内容", "请输入日志格式", 2)
                LoggingFormatSetting.delete(0, END)
                LoggingFormatSetting.insert(END, LOG_FORMAT)
                Format = LOG_FORMAT
                logging.info("[设置 - 日志格式] 由于格式框为空，已恢复到原格式")
                is_save = False
                logging.info("[设置] 已关闭设置保存")
                if Format == DLOG_FORMAT:  # 日志格式无变化
                    is_save_format = False
                    logging.info("[设置 - 日志格式] 已关闭设置日志格式保存")
            # == 日志格式 == #

            try:
                # == 日志格式 == #
                if is_save_format: # 日志格式
                    Set_Format = {"Format": Format}
                else:
                    Set_Format = {}
                logging.debug("[设置 - 日志格式] 格式已确定为 " + str(Set_Format))
                # == 日志格式 == #

                Set = dict(Set_Format) # 设置合并
                logging.debug("[设置] 设置已确定为 " + str(Set))
                if Set == {}:
                    logging.info("[设置] 无设置更改，准备关闭设置窗口")
                    if is_save:
                        set.destroy() # 关闭
                        logging.info("[设置] 已关闭设置窗口")
                    is_save = False
                    logging.info("[设置] 已关闭设置保存")
                if not message("是否要保存设置", "保存设置后可能使应用重启", 4):
                    is_save = False
                    logging.info("[设置] 已关闭设置保存")
                if is_save:
                    with open("DEF/set.json", "w") as S:
                        json.dump(Set, S) # 储存
            except UnboundLocalError:
                message("错误：有输入框中无内容", sys.exc_info()[1], 3)
            ## ==== 数据储存 ==== ##

            ## ==== 调试模式 ==== ##
            if CheckDebug.get() == 1:
                is_log = True  if str(logging.getLogger("levelname")) != '<Logger levelname (DEBUG)>' else False
                logging.getLogger().setLevel(logging.DEBUG) # 日志设置
                logging.info("[设置-调试模式] 已开启调试模式") if is_log else ""
                is_reboot = False
            else:
                is_log = True  if str(logging.getLogger("levelname")) == '<Logger levelname (DEBUG)>' else False
                logging.getLogger().setLevel(logging.INFO)  # 日志设置
                logging.info("[设置-调试模式] 已关闭调试模式") if is_log else ""
            ## ==== 调试模式 ==== ##
            logging.info("[设置] 已保存设置")
            if is_save:
                set.destroy()
                if is_reboot:
                    Reboot()

        set = Toplevel(root)
        set.geometry('320x400')
        set.minsize(320, 400)
        set.title("设置")
        logging.info("[设置] 设置窗口已开启")

        # 日志设置
        LoggingSettingTitle = Label(set, text="日志设置", font=("微软雅黑", 10, "bold"))
        LoggingSettingTitle.place(relx=0.03, rely=0.01)
        # 日志格式
        LoggingFormatSettingTitle = Label(set, text="格式设置")
        LoggingFormatSettingTitle.place(relx=0.1, rely=0.06)
        LoggingFormatSetting = Entry(set)
        LoggingFormatSetting.place(relx=0.3, rely=0.065, relwidth=0.65, height=20)
        # 格式读取
        LoggingFormatSetting.delete(0, END)
        LoggingFormatSetting.insert(END, LOG_FORMAT)
        # 调试模式
        CheckDebug = IntVar()
        Debug = Checkbutton(set, text='调试模式', variable=CheckDebug, onvalue=1, offvalue=0)
        Debug.place(relx=0.03, rely=0.93)
        if str(logging.getLogger("levelname")) == '<Logger levelname (DEBUG)>':
            Debug.select()
            logging.info("[设置-调试模式] 检测到已开启调试模式")
        else:
            Debug.deselect()
            logging.info("[设置-调试模式] 检测到已关闭调试模式")

        # 恢复默认设置
        Button(set, text="重置", command=Reset).place(relx=0.50, rely=0.93,relwidth=0.23, relheight=0.05)
        # 确认按钮
        Button(set, text="确定", command=Fix).place(relx=0.75, rely=0.93,relwidth=0.23, relheight=0.05)

    def Exit():
        root.destroy()

    root = Tk()
    root.minsize(350, 460)
    root.geometry("360x480")
    root.title("删除空文件夹 & 空文件")
    logging.info("[DEF] 应用已启动")


    ## ==== 菜单栏 ==== ##
    mainmenu = Menu(root)
    menuFile = Menu(mainmenu, tearoff=0) # 菜单分组 menuFile
    mainmenu.add_cascade(label="文件", menu=menuFile)
    menuFile.add_command(label="添加文件", command=DiaFolder)

    menuApp = Menu(mainmenu, tearoff=0)  # 菜单分组 menuApp
    mainmenu.add_cascade(label="应用", menu=menuApp)
    menuApp.add_command(label="设置", command=Setting)
    menuApp.add_command(label="重启", command=Reboot)
    menuApp.add_command(label="退出", command=Exit)
    root.config(menu=mainmenu)

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

    ExpansionComponents()
    DiaFolder()
    root.mainloop()
    logging.info("[DEF] 应用已关闭")
except:
    message(f"错误:{sys.exc_info()[0]}", str(sys.exc_info()[1]), 3)