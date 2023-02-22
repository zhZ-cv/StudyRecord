# -*- codeing = utf-8 -*-
# @Time : 2022/9/5 10:02
# @Author : MOTR
# @File : logPrint.py
# @Software : PyCharm
import time
import os


class logPrint:
    def __init__(self, fileName):
        self.fileName = fileName
        if os.name == 'nt':
            os.system('')

    def print(self, printData, msg):
        printColor = printData[0]
        printType = printData[1]
        printTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print(f'\x1b[1;97;40m {printTime} \033[0m{printColor} [{printType}]{self.fileName} {msg}\033[0m')

    def input(self, printData, msg):
        printColor = printData[0]
        printType = printData[1]
        printTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        dataWords = input(f'\x1b[1;97;40m {printTime} \033[0m{printColor} [{printType}]{self.fileName} {msg}\033[0m')
        return dataWords
