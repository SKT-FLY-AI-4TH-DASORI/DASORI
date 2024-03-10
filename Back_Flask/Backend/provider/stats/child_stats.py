from flask import jsonify
from datetime import datetime
import model.__init__ as db

db.init_db()

# ----- Class 선언부 ----- #
# ReportServiceChild - 아이 통계 호출 함수


# (GET) /reports
# 제공 화면: 통계 화면
class ReportServiceChild:
    def __init__(self, pid):
        self.pid = pid

    # 아이 Today 통계 불러오기
    def get_day1_report(self, pid):
        date = datetime.now().date()
        child_diary = db.get_child_diary(pid, date)

        mood = child_diary.cd_mood
        correctedRatio = child_diary.cd_correctRatio

        return {"day1_mood": mood, "day1_correct": correctedRatio}

    # 아이 최신 7개 ratio를 받아오기
    def get_day7_report(self, pid):
        correctedRatio, mood, dateList = db.get_recent7_child_stats(pid)

        mood_list, correct_list, date_list = [], [], []

        for i in range(len(mood)):
            mood_list.append(mood[i].cd_mood)
            correct_list.append(correctedRatio[i].cd_correctRatio)
            date_list.append(dateList[i].cd_date)

        return {
            "day7_mood": mood_list,
            "day7_correct": correct_list,
            "day7_dateList": date_list,
        }

    # 아이 최신 30개 ratio를 받아오기
    def get_day30_report(self, pid):
        correctedRatio, dateList = db.recent30_child_stats(pid)

        correct_list, date_list = [], []

        for i in range(len(correctedRatio)):
            correct_list.append(correctedRatio[i].cd_correctRatio)
            date_list.append(dateList[i].cd_date)

        return {"day30_correct": correct_list, "day30_dateList": date_list}

    # def result_code(self):
    #     isSuccess =
    #     code =
    #     message =
