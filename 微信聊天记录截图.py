"""
微信聊天记录截图
连接手机 使用命令符的adb截图
主要功能是滚动屏幕并截图，同时把图片传到电脑
"""

import os
import time
from PIL import Image


def execute(cmd):
    adbstr = 'adb {}'.format(cmd)
    print(adbstr)
    os.system(adbstr)


if __name__ == '__main__':
    i = 999
    savedir = r'/Users/Gavin/Desktop/20210805微信聊天记录导出备份/聊天记录分析_pyhton/screen/'
    while True:
        i = i + 1
        # 截图
        execute("shell screencap /sdcard/临时/screen/"+str(i)+".png")
        execute("pull /sdcard/临时/screen/"+str(i)+".png  " + savedir)

        try:
            os.rename(savedir+str(i), savedir+str(i)+".png")
        except Exception as e:
            print(e)
            print('rename file fail\r\n')
        else:
            print('rename file success\r\n')

        # 滑动 adb shell input swipe x1 y1 x2 y2
        execute("shell input swipe 400 2070 400 1542 200")

        # 自动除去头尾
        img = Image.open(savedir+str(i)+".png")
        print(img.size)
        cropped = img.crop((0, 221, 1080, 2188))  # (left, upper, right, lower)
        cropped.save(savedir+str(i)+".png")

        time.sleep(0.1)
