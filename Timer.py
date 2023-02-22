# -*- codeing = utf-8 -*-
# @Time : 2022/9/8 10:53
# @Author : MOTR
# @File : Timer.py
# @Software : PyCharm
import json
import time

import pymysql


class Timer:
    def __init__(self, Date):
        timeRecordFile = open('timeRecord.json', 'r', encoding='utf-8')
        self.timeDict = json.load(timeRecordFile)
        timeRecordFile.close()
        self.Date = Date
        self.lastTime = 0
        try:
            self.todayStudyTime = self.timeDict['data']['perDayTime'][self.Date]['studyTime']
            self.todayNoteTime = self.timeDict['data']['perDayTime'][self.Date]['noteTime']
            self.todayExerciseTime = self.timeDict['data']['perDayTime'][self.Date]['exerciseTime']
            self.todayRestTime = self.timeDict['data']['perDayTime'][self.Date]['restTime']
        except:
            self.initTodayTime()
        self.studyTimeSum = self.timeDict['data']['studyTimeSum']
        self.noteTimeSum = self.timeDict['data']['noteTimeSum']
        self.exerciseTimeSum = self.timeDict['data']['exerciseTimeSum']
        self.restTimeSum = self.timeDict['data']['restTimeSum']
        self.detailed = []

    def initTodayTime(self):
        self.timeDict['data']['perDayTime'][self.Date] = {}
        self.timeDict['data']['perDayTime'][self.Date]['studyTime'] = 0
        self.timeDict['data']['perDayTime'][self.Date]['noteTime'] = 0
        self.timeDict['data']['perDayTime'][self.Date]['exerciseTime'] = 0
        self.timeDict['data']['perDayTime'][self.Date]['restTime'] = 0
        self.todayStudyTime = 0
        self.todayNoteTime = 0
        self.todayExerciseTime = 0
        self.todayRestTime = 0

    def Study(self, studyCourse):
        self.todayStudyTime += 1
        self.studyTimeSum += 1
        detailedTime = (int(time.time()), 1, studyCourse)
        self.detailed.append(detailedTime)

    def Note(self, studyCourse):
        self.todayNoteTime += 1
        self.noteTimeSum += 1
        detailedTime = (int(time.time()), 2, studyCourse)
        self.detailed.append(detailedTime)

    def Exercise(self, studyCourse):
        self.todayExerciseTime += 1
        self.exerciseTimeSum += 1
        detailedTime = (int(time.time()), 3, studyCourse)
        self.detailed.append(detailedTime)

    def Rest(self, studyCourse):
        self.todayRestTime += 1
        self.restTimeSum += 1
        detailedTime = (int(time.time()), 4, studyCourse)
        self.detailed.append(detailedTime)

    def update(self):
        lastUpdateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if self.Date not in lastUpdateTime:
            self.initTodayTime()
            self.Date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        timeRecordFile = open('timeRecord.json', 'w+', encoding='utf-8')
        self.timeDict['data']['studyTimeSum'] = self.studyTimeSum
        self.timeDict['data']['noteTimeSum'] = self.noteTimeSum
        self.timeDict['data']['exerciseTimeSum'] = self.exerciseTimeSum
        self.timeDict['data']['restTimeSum'] = self.restTimeSum
        self.timeDict['data']['perDayTime'][self.Date]['studyTime'] = self.todayStudyTime
        self.timeDict['data']['perDayTime'][self.Date]['noteTime'] = self.todayNoteTime
        self.timeDict['data']['perDayTime'][self.Date]['exerciseTime'] = self.todayExerciseTime
        self.timeDict['data']['perDayTime'][self.Date]['restTime'] = self.todayRestTime
        self.timeDict['lastUpdateTime'] = lastUpdateTime
        json.dump(self.timeDict, timeRecordFile)
        timeRecordFile.close()

    def uploadDetailedTime(self):
        detailedCopy = self.detailed
        self.detailed = []
        newTime = detailedCopy[0][0]
        while self.lastTime >= newTime:
            detailedCopy.pop(0)
            newTime = detailedCopy[0][0]
        con = pymysql.connect(host='81.68.127.249', port=3306,
                              user='root', password='Motr302030150.',
                              db='StudyRecord', charset='utf8')
        try:
            with con.cursor() as cursor:
                cursor.execute(f"select course from LastInformation")
                for i in detailedCopy:
                    detailedT = i[0]
                    statusID = i[1]
                    studyCourseID = i[2]
                    cursor.execute(f"insert into DetailedTime values({detailedT}, {statusID}, {studyCourseID})")
                con.commit()
                self.lastTime = detailedCopy[len(detailedCopy) - 1][0]
        except:
            pass
        finally:
            con.close()
