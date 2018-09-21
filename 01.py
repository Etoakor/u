import psutil
import time,sys
import webbrowser
import pyttsx3



#/*
# *  ---全局数据 实时更新
# */
local_device = []                   #本地驱动器
local_letter = []                   #本地盘符
local_number = 0                    #本地驱动器数
mobile_device = []                  #移动设备
mobile_letter = []                  #移动设备盘符
mobile_number = 0                   #移动设备数


def updata():
    global local_device, local_letter, local_number, \
        mobile_device, mobile_letter, mobile_number
    # 引入全局变量
    tmp_local_device, tmp_local_letter = [], []
    tmp_mobile_device, tmp_mobile_letter = [], []
    tmp_local_number, tmp_mobile_number = 0, 0

    try:
        part = psutil.disk_partitions()
    except:
        print("程序发生异常!!!")
       # box(None, "很抱歉，程序发生了异常", "致命错误", 0)
        sys.exit(-1)
    else:
        # * 驱动器分类
        for i in range(len(part)):
            tmplist = part[i].opts.split(",")
            if tmplist[1] == "fixed":  # 挂载选项数据内读到fixed = 本地设备
                tmp_local_number = tmp_local_number + 1
                tmp_local_letter.append(part[i].device[:2])  # 得到盘符信息
                tmp_local_device.append(part[i])
            else:
                tmp_mobile_number = tmp_mobile_number + 1
                tmp_mobile_letter.append(part[i].device[:2])
                tmp_mobile_device.append(part[i])

        # *浅切片
        local_device, local_letter = tmp_local_device[:], tmp_local_letter[:]
        mobile_device, mobile_letter = tmp_mobile_device[:], tmp_mobile_letter[:]
        local_number, mobile_number = tmp_local_number, tmp_mobile_number

    return len(part)  # 返回当前驱动器数


def print_device(n):
    global local_device, local_letter, local_number, \
        mobile_device, mobile_letter, mobile_number

    print("=" * 50 + "\n读取到" + str(n) + "个驱动器")
    for l in range(local_number):
        print(local_letter[l], end="")  # 列出本地驱动器盘符
    # print("{" + local_device[0].opts + "}")
    if (len(mobile_device)):  # 列出移动驱动器盘符
        for m in range(mobile_number):
           print(mobile_letter[m], end="")
        print("{" + mobile_device[0].opts + "}")
    else:
        None

    print("进程进入监听状态 " + "*" * 10)
    return

if __name__ == "__main__":
    #*初次读取驱动器信息，打印驱动器详细
    now_number = 0                  #实时驱动数
    before_number = updata()        #更新数据之前的驱动数
    print_device(before_number)
    #进程进入循环 Loop Seconds = 1s

    while True:
        now_number = updata()
        if(now_number > before_number):
            print("检测到移动磁盘被插入...")
            print_device(now_number)
            engine = pyttsx3.init()
            engine.say('警告！警告！！警告！！！有人正在插入U盘盗取文件！')
            engine.runAndWait()

            webbrowser.open("http://www.etoakor.com")
            before_number = now_number                  #刷新数据
        elif(now_number < before_number):
            print("检测到移动磁盘被拔出...")
            print_device(now_number)
           # box(None,"移动磁盘被拔出\n","磁盘被拔出",0)
            engine = pyttsx3.init()
            engine.say('警告！警告！！警告！！！有人正在拔取U盘盗取文件！')
            engine.runAndWait()
            webbrowser.open("http://www.etoakor.com")
            before_number = now_number
        time.sleep(1)



        # pyinstaller -F -p C:\Users\DELL\PycharmProjects\u\venv\Lib\site-packages -i favicon.ico 1.py
        # pyinstaller -F -i favicon.ico 1.py
        # pyinstaller 1.spec