# -*- codeing = utf-8 -*-
# @Time : 2022/9/14 15:29
# @Author : MOTR
# @File : StudyRecord.py
# @Software : PyCharm
import json
import random
import re
import time
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from log import logPrint, logType
import threading
import keyboard
import Timer

LP = logPrint.logPrint('')
LT = logType.logType
courseInformation = {'Math': 1, 'LA': 2, 'Politics': 3, 'DS': 4, 'OS': 5, 'POCC': 6, 'CN': 7}
# 这里修改成自己的链接
exerciseUrl = {'Math': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F07%E3%80%81%E5%90%AF%E8%88%AA'
                       '%EF%BC%88%E5%BC%A0%E5%AE%87%20%E9%AB%98%E6%98%86%E4%BB%91%EF%BC%89%2F00.%E6%89%AB%E6%8F%8F%E8'
                       '%AE%B2%E4%B9%89%2F%E3%80%90%E5%BC%A0%E5%AE%87%E3%80%91%E8%80%83%E7%A0%94%E6%95%B0%E5%AD%A6%E5'
                       '%9F%BA%E7%A1%8030%E8%AE%B2%EF%BC%88%E9%AB%98%E7%AD%89%E6%95%B0%E5%AD%A6%E5%88%86%E5%86%8C%EF'
                       '%BC%89.pdf&fsid=146704681785019&size=367701975',
               'LA': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F07%E3%80%81%E5%90%AF%E8%88%AA'
                     '%EF%BC%88%E5%BC%A0%E5%AE%87%20%E9%AB%98%E6%98%86%E4%BB%91%EF%BC%89%2F00.%E6%89%AB%E6%8F%8F%E8'
                     '%AE%B2%E4%B9%89%2F%E3%80%90%E5%BC%A0%E5%AE%87%E3%80%91%E8%80%83%E7%A0%94%E6%95%B0%E5%AD%A6%E5'
                     '%9F%BA%E7%A1%8030%E8%AE%B2%EF%BC%88%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0%E5%88%86%E5%86%8C%EF%BC'
                     '%89.pdf&fsid=823722557346854&size=175888438',
               'Politics': '',
               'DS': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F2023%E3%80%90%E7%8E%8B%E9%81%93'
                     '%E3%80%91%E8%AE%A1%E7%AE%97%E6%9C%BA408%E9%A2%86%E5%AD%A6%E7%8F%AD%E3%80%90%E6%8E%A8%E8%8D%90'
                     '%E3%80%91%2F2023%E7%8E%8B%E9%81%93%E3%80%8A%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E3%80%8B%E8%80'
                     '%83%E7%A0%94%E5%A4%8D%E4%B9%A0%E6%8C%87%E5%AF%BC%E3%80%90%E5%B0%8F%E9%BA%A6%E9%BA%A6%E8%B5%84'
                     '%E6%96%99%E5%BA%93%E3%80%91.pdf&fsid=783274408810197&size=186658531',
               'OS': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F2023%E3%80%90%E7%8E%8B%E9%81%93'
                     '%E3%80%91%E8%AE%A1%E7%AE%97%E6%9C%BA408%E9%A2%86%E5%AD%A6%E7%8F%AD%E3%80%90%E6%8E%A8%E8%8D%90'
                     '%E3%80%91%2F2023%E7%8E%8B%E9%81%93%E3%80%8A%E6%93%8D%E4%BD%9C%E7%B3%BB%E7%BB%9F%E3%80%8B%E5%A4'
                     '%8D%E4%B9%A0%E6%8C%87%E5%AF%BC.pdf&fsid=90560906248094&size=168847144',
               'POCC': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F2023%E3%80%90%E7%8E%8B%E9%81'
                       '%93%E3%80%91%E8%AE%A1%E7%AE%97%E6%9C%BA408%E9%A2%86%E5%AD%A6%E7%8F%AD%E3%80%90%E6%8E%A8%E8%8D'
                       '%90%E3%80%91%2F2023%E7%8E%8B%E9%81%93%E3%80%8A%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BB%84%E6%88%90'
                       '%E5%8E%9F%E7%90%86%E3%80%8B%E8%80%83%E7%A0%94%E5%A4%8D%E4%B9%A0%E6%8C%87%E5%AF%BC.pdf&fsid'
                       '=691528813941386&size=156583192',
               'CN': 'https://pan.baidu.com/disk/pdfview?path=%2F%E8%80%83%E7%A0%94%2F2023%E3%80%90%E7%8E%8B%E9%81%93'
                     '%E3%80%91%E8%AE%A1%E7%AE%97%E6%9C%BA408%E9%A2%86%E5%AD%A6%E7%8F%AD%E3%80%90%E6%8E%A8%E8%8D%90'
                     '%E3%80%91%2F2023%E7%8E%8B%E9%81%93%E3%80%8A%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%BD%91%E7%BB%9C%E3%80'
                     '%8B%E8%80%83%E7%A0%94%E5%A4%8D%E4%B9%A0%E6%8C%87%E5%AF%BC.pdf&fsid=738240147764249&size'
                     '=146576552'}


class Study:
    def __init__(self, course):
        self.Course = course
        self.CourseID = courseInformation[course]
        # 判断是不是进入了学习模式
        self.isStudying = False
        # 判断是不是进入了做笔记模式
        self.isNoting = False
        # 判断是不是进入了刷题模式
        self.isExercising = False
        # 判断是不是进入了休息模式
        self.isResting = False
        # 获取上次视频播放的链接
        lastInformationFile = open('lastInformation.json', 'r', encoding='utf-8')
        self.lastViewJS = json.load(lastInformationFile)
        self.lastViewData = self.lastViewJS['data']
        self.lastUrl = self.lastViewData[self.Course]['lastViewUrl']
        lastInformationFile.close()

    # 更新最新的观看链接
    def updateLastViewUrl(self):
        lastInformationFile = open('lastInformation.json', 'w', encoding='utf-8')
        self.lastViewJS['lastUpdateTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.lastViewData[self.Course]['lastViewUrl'] = self.lastUrl
        json.dump(self.lastViewJS, lastInformationFile)
        lastInformationFile.close()

    # 对学习链接解析得到学习的内容
    def getDataRecords(self, URL):
        DataRecords1 = unquote(URL, 'utf-8').replace(
            'https://pan.baidu.com/play/video#/video?path=/考研/', '')
        DataRecords = re.sub(re.compile(r'&t=(.*)'), '', DataRecords1)
        DataRecords1 = DataRecords.replace('/', '-')
        DataRecords = re.sub(re.compile(r'-\d+\.'), '-', DataRecords1)
        return DataRecords

    # 将学习情况的数据更新至json文件
    def recordStudyInformation(self, mode, DataRecords):
        presentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        studyInformationFile = open('studyInformation.json', 'r', encoding='utf-8')
        rawInformation = json.load(studyInformationFile)
        studyInformationFile.close()
        rawInformation['lastUpdateTime'] = presentTime
        studyInformation = {"time": presentTime, "course": self.Course, "mode": mode,
                            "task": DataRecords}
        rawInformation['data'].append(studyInformation)
        studyInformationFile = open('studyInformation.json', 'w', encoding='utf-8')
        json.dump(rawInformation, studyInformationFile, ensure_ascii=False)
        studyInformationFile.close()

    # 学习模式
    def Studying(self):
        self.isStudying = True
        wb.execute_script(f"window.open('{self.lastUrl}', '_parent');")
        LP.print(LT.Normal, '进入学习模式！')
        times = 0
        while self.isStudying:
            T.Study(self.CourseID)
            times += 1
            if times == 60:
                DataRecords = self.getDataRecords(self.lastUrl)
                LP.print(LT.Study, DataRecords)
                self.recordStudyInformation('休息模式', DataRecords)
                times = 0
            currentUrl = wb.current_url
            if currentUrl != self.lastUrl:
                self.lastUrl = currentUrl
                self.updateLastViewUrl()
            time.sleep(1)
        LP.print(LT.Normal, '学习模式结束！')

    # 笔记模式
    def Noting(self):
        self.isNoting = True
        LP.print(LT.Normal, '进入笔记模式！')
        DataRecords = self.getDataRecords(self.lastUrl)
        times = 0
        while self.isNoting:
            T.Note(self.CourseID)
            times += 1
            if times == 10:
                LP.print(LT.Note, DataRecords)
                self.recordStudyInformation('笔记模式', DataRecords)
                times = 0
            time.sleep(1)
        LP.print(LT.Normal, '笔记模式结束！')

    # 刷题模式
    def Exercising(self):
        self.isExercising = True
        wb.execute_script(f"window.open('{exerciseUrl[self.Course]}', '_parent');")
        LP.print(LT.Normal, '进入刷题模式！')
        DataRecords = self.getDataRecords(self.lastUrl)
        times = 0
        while self.isExercising:
            T.Exercise(self.CourseID)
            times += 1
            if times == 60:
                LP.print(LT.Exercise, DataRecords)
                self.recordStudyInformation('刷题模式', DataRecords)
                times = 0
            time.sleep(1)
        LP.print(LT.Normal, '刷题模式结束！')

    # 休息模式时执行的函数
    def Resting(self):
        self.isResting = True
        LP.print(LT.Normal, '进入休息模式！')
        DataRecords = self.getDataRecords(self.lastUrl)
        times = 0
        while self.isResting:
            T.Rest(self.CourseID)
            times += 1
            if times == 60:
                LP.print(LT.Rest, '当前处于休息模式...')
                self.recordStudyInformation('休息模式', DataRecords)
                times = 0
            time.sleep(1)
        LP.print(LT.Normal, '休息模式结束！')


# 监听模式的结束
def listenModeChangeEvent():
    keyboard.wait('`')
    studyCourse.isStudying = False
    studyCourse.isNoting = False
    studyCourse.isExercising = False
    studyCourse.isResting = False


# 实时更新时间数据
def updateTime():
    uploadTime = 0
    while not isKilled:
        randomNum = random.randint(1, 3)
        time.sleep(randomNum)
        uploadTime += randomNum
        if uploadTime >= 300:
            T.uploadDetailedTime()
            uploadTime = 0
        else:
            T.update()
    if uploadTime != 0:
        T.uploadDetailedTime()


def secondsToTime(totalSeconds):
    hours = int(totalSeconds / 3600)
    minutes = int((totalSeconds - hours * 3600) / 60)
    seconds = totalSeconds - hours * 3600 - minutes * 60
    Time = f'{hours}h {minutes}m {seconds}s'
    return Time


if __name__ == '__main__':
    Date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    T = Timer.Timer(Date)
    Course = LP.input(LT.Normal, '请输入要开始学习的课程：')
    chrome_options = Options()
    # 这里填你自己的浏览器缓存地址，例如：user-data-dir=C:\Users\yourName\AppData\Local\Google\Chrome\User Data
    chrome_options.add_argument('')
    chrome_options.add_argument('disable-infobars')
    wb = webdriver.Chrome(options=chrome_options)
    studyCourse = Study(Course)
    isKilled = False
    try:
        updateTimeThread = threading.Thread(target=updateTime)
        updateTimeThread.start()
        while True:
            LP.print(LT.Study, '[1]学习模式')
            LP.print(LT.Note, '[2]笔记模式')
            LP.print(LT.Exercise, '[3]刷题模式')
            LP.print(LT.Rest, '[4]休息模式')
            mode = LP.input(LT.Normal, '请输入需要进入的模式：')
            listenModeChangeEventThread = threading.Thread(target=listenModeChangeEvent)
            if '1' == mode:
                listenModeChangeEventThread.start()
                studyCourse.Studying()
                nextUrl = LP.input(LT.Normal, '请输入下一章节的链接：')
                if 'https://pan.baidu.com' in nextUrl:
                    studyCourse.lastUrl = nextUrl
                    studyCourse.updateLastViewUrl()
            elif '2' == mode:
                listenModeChangeEventThread.start()
                studyCourse.Noting()
            elif '3' == mode:
                listenModeChangeEventThread.start()
                studyCourse.Exercising()
            elif '4' == mode:
                listenModeChangeEventThread.start()
                studyCourse.Resting()
            elif '5' == mode:
                listenModeChangeEventThread.start()
                Course = LP.input(LT.Normal, '请输入需要学习的课程：')
                studyCourse = Study(Course)
            else:
                # wb.close()
                isKilled = True
                LP.print(LT.Warning, '正在上传本次的学习数据，请耐心等待上传结束！')
                todayStudyTime = secondsToTime(T.todayStudyTime)
                totalStudyTime = secondsToTime(T.studyTimeSum)
                todayNoteTime = secondsToTime(T.todayNoteTime)
                totalNoteTime = secondsToTime(T.noteTimeSum)
                todayExerciseTime = secondsToTime(T.todayExerciseTime)
                totalExerciseTime = secondsToTime(T.exerciseTimeSum)
                todayRestTime = secondsToTime(T.todayRestTime)
                totalRestTime = secondsToTime(T.restTimeSum)
                LP.print(LT.Normal, f'今日时间分配情况：')
                LP.print(LT.Study, f'学习时长：{todayStudyTime}')
                LP.print(LT.Note, f'笔记时长：{todayNoteTime}')
                LP.print(LT.Exercise, f'刷题时长：{todayExerciseTime}')
                LP.print(LT.Rest, f'休息时长：{todayRestTime}')
                LP.print(LT.Normal, f'总时间分配情况：')
                LP.print(LT.Study, f'总学习时长：{totalStudyTime}')
                LP.print(LT.Note, f'总笔记时长：{totalNoteTime}')
                LP.print(LT.Exercise, f'总刷题时长：{totalExerciseTime}')
                LP.print(LT.Rest, f'总休息时长：{totalRestTime}')
                LP.print(LT.Success, '本次学习到此结束！期待下次的学习！')
                break
    except:
        isKilled = True
        LP.print(LT.Warning, '检测到异常关闭，关闭前上传最新学习数据')
        T.update()
