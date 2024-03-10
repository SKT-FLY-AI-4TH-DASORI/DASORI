from flask import jsonify
from datetime import datetime
import model.__init__ as db

db.init_db()

# ----- Class 선언부 ----- #
# ReportServiceParent - 부모 통계 호출 함수


# (GET) /reports
# 제공 화면: 통계 화면
class ReportServiceParent:
    def __init__(self, pid):
        self.pid = pid

    # 부모 Today 통계 불러오기
    def get_day1_report(self, pid):
        # db check
        date = datetime.now().date()
        parent_diary = db.get_parent_diary(pid, date)

        languageRatio = parent_diary.pd_langRatio
        correctedRatio = parent_diary.pd_correctRatio

        return {"day1_lang": languageRatio, "day1_correct": correctedRatio}

    # 부모 최신 7개 ratio를 받아오기
    def get_day7_report(self, pid):
        languageRatio, correctedRatio, dateList = db.get_recent7_parent_stats(pid)

        lang_list, correct_list, date_list = [], [], []

        for i in languageRatio:
            lang_list.append(i.pd_langRatio)
        for i in correctedRatio:
            correct_list.append(i.pd_correctRatio)
        for i in dateList:
            date_list.append(i.pd_date)

        # for i in range(len(languageRatio)):
        #     lang_list.append(languageRatio[i].pd_langRatio)
        #     correct_list.append(correctedRatio[i].pd_correctRatio)
        #     date_list.append(dateList.pd_date[i])

        return {
            "day7_lang": lang_list,
            "day7_correct": correct_list,
            "day7_dateList": date_list,
        }

    # 부모 최신 30개 ratio를 받아오기
    def get_day30_report(self, pid):
        languageRatio, correctedRatio, dateList = db.recent30_parent_stats(pid)

        lang_list, correct_list, date_list = [], [], []

        for i in languageRatio:
            lang_list.append(i.pd_langRatio)
        for i in correctedRatio:
            correct_list.append(i.pd_correctRatio)
        for i in dateList:
            date_list.append(i.pd_date)

        # for i in range(len(languageRatio)):
        #     lang_list.append(languageRatio[i].pd_langRatio)
        #     #correct_list.append(correctedRatio[i].pd_correctRatio)
        #     date_list.append(dateList[i].pd_date)

        return {
            "day30_lang": lang_list,
            "day30_correct": correct_list,
            "day30_dateList": date_list,
        }

    # def result_code(self):
    #     isSuccess =
    #     code =
    #     message =
