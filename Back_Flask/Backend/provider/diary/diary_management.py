from flask import jsonify
from datetime import datetime
import model.__init__ as db
import sys

# sys.path.append("..")
from provider.ml_api_handler import *

db.init_db()


# ----- Class 선언부 ----- #
# DiaryService - 홈 화면 관련 호출 함수
class DiaryService:
    """
    get_complete_list()
    get_parent_diary_preview()
    get_child_diary_preview()
    """

    def __init__(self, date, pid):
        # date = datetime.strptime(date_string, "%Y-%m-%d")
        self.date = date
        self.pid = pid

    # (GET) /home
    # 한달 기준 일기 작성된 일자 불러오기
    # 제공 화면: 홈 화면(달력)
    def get_complete_list(self):
        complist = []
        completeList = db.get_date(self.pid, self.date)
        for i in completeList:
            complist.append(i.pd_date)
        return complist  # list(datetime)

    # (GET) /home, /home/selectedDate
    # 특정 일자 부모 일기 미리보기 가져오기
    # 제공 화면: 홈 화면(부모 일기 미리보기 칸)
    def get_parent_diary_preview(self):
        parent_diary = db.get_parent_diary(self.pid, self.date)
        if parent_diary is None:
            return {
                "correctedText": "",
                "translatedText": "",
                "imageUrl": "",
            }
        correctedText = parent_diary.pd_corrected
        translatedText = parent_diary.pd_translated
        imageUrl = db.get_image_s3(parent_diary.pd_imageURL)

        return {
            "correctedText": correctedText,
            "translatedText": translatedText,
            "imageUrl": imageUrl,
        }

    # (GET) /home
    # 특정 일자 아이 일기 미리보기 가져오기
    # 제공 화면: 홈 화면(아이 일기 미리 보기 칸)
    def get_child_diary_preview(self):
        child_diary = db.get_child_diary(self.pid, self.date)
        if child_diary is None:
            return {
                "correctedText": "",
                "translatedText": "",
                "imageUrl": "",
            }
        correctedText = child_diary.cd_corrected
        translatedText = child_diary.cd_translated
        imageUrl = db.get_image_s3(child_diary.cd_imageURL)

        return {
            "correctedText": correctedText,
            "translatedText": translatedText,
            "imageUrl": imageUrl,
        }

    # def result_code(self):
    #     isSuccess =
    #     code =
    #     message =


# ----- 기타 함수 호출부 ----- #


#  1. 소통화면 관련 함수  #
# (GET) /home/conversation
# 특정 일자 부모 일기 가져오기
# 제공 화면: 소통 화면(부모 일기 보기 칸)
def choosing_parent_diary(date, pid):
    # date = datetime.strptime(date_string, "%Y-%m-%d")
    parent_diary = db.get_parent_diary(pid, date)
    correctedText = parent_diary.pd_corrected
    translatedText = parent_diary.pd_translated
    imageUrl = db.get_image_s3(parent_diary.pd_imageURL)
    characterUrl_parent = db.get_image_s3(parent_diary.pd_charURL)
    print("======convParent", characterUrl_parent)
    question_parent = parent_diary.pd_question
    text = parent_diary.pd_text

    if parent_diary is None:
        return {
            "correctedText": "",
            "translatedText": "",
            "imageUrl": "",
            "characterUrl": "",
            "question": "",
            "text": "",
        }

    return {
        "correctedText": correctedText,
        "translatedText": translatedText,
        "imageUrl": imageUrl,
        "characterUrl": characterUrl_parent,
        "question": question_parent,
        "text": text,
    }


# (GET) /home/conversation
# 특정 일자 아이 일기 가져오기
# 제공 화면: 소통 화면(아이 일기 보기 칸)
def choosing_child_diary(date, pid):
    # date = datetime.strptime(date_string, "%Y-%m-%d")
    child_diary = db.get_child_diary(pid, date)
    correctedText = child_diary.cd_corrected
    translatedText = child_diary.cd_translated
    imageUrl = db.get_image_s3(child_diary.cd_imageURL)
    characterUrl_child = db.get_image_s3(child_diary.cd_charURL)
    print("======convChild", characterUrl_child)
    question_child = child_diary.cd_question

    if child_diary is None:
        return {
            "correctedText": "",
            "translatedText": "",
            "imageUrl": "",
            "characterUrl": "",
            "question": "",
        }

    return {
        "correctedText": correctedText,
        "translatedText": translatedText,
        "imageUrl": imageUrl,
        "characterUrl": characterUrl_child,
        "question": question_child,
    }


#  2. 일기 작성 관련  #
# (POST) /home/parent
# 부모 일기 작성
# 제공 화면: 부모 일기 작성 화면
def writing_parent_diary(pid, date, text, image):
    # date = datetime.now().date()

    imageUrl = db.set_image_s3(image)
    return_imgURL = db.get_image_s3(imageUrl)

    # print("-----date", date_string, type(date_string))
    # date = datetime.strptime(date_string, "%Y-%m-%d")

    # @ 무너 api
    kor_translatedText = pd_translator(text)
    print("==================kor_translatedText")
    correctedText = kor_correct(kor_translatedText)
    print("==================correctedText")
    translatedText = diary_translator(correctedText, "ko", "vi")
    print("==================translatedText")
    charImg = create_image(correctedText)
    print("==================create_image")
    charImgUrl = db.set_image_s3(charImg)
    print("==================set_image_s3")
    corretRatio = correctRatio(diary_translator(text, "vi", "ko"), correctedText)
    print("==================corretRatio")
    langRatio = translate_ratio(text)
    print("==================langRatio")
    question = create_question(correctedText)
    print("==================question")

    db.set_parent_diary(
        pid,
        date,
        text,
        correctedText,
        translatedText,
        imageUrl,
        charImgUrl,
        langRatio,
        corretRatio,
        question,
    )

    return (correctedText, translatedText, return_imgURL, text)


# (POST) /home/child
# 아이 일기 작성
# 제공 화면: 부모 일기 작성 화면
def writing_child_diary(pid, date, image):
    # date = datetime.now().date()
    # date = datetime.strptime(date_string, "%Y-%m-%d")
    imageUrl = db.set_image_s3(image)  # 파일 이름 반환
    saved_imgurl = db.get_image_s3(imageUrl)  # url 반환

    # @ 무너 api
    ocr_text = clova_ocr(saved_imgurl)
    print("1")
    correctedText = kor_correct(ocr_text)
    print("2")
    translatedText = diary_translator(correctedText, "ko", "vi")
    print("3")
    charImg = create_image(correctedText)
    print("4")
    charImgUrl = db.set_image_s3(charImg)
    print("5")
    corretRatio = correctRatio(ocr_text, correctedText)
    print("6")
    moodRatio = mood(correctedText)
    print("7")
    question = create_question(correctedText)
    print("8")

    db.set_child_diary(
        pid,
        date,
        correctedText,
        translatedText,
        imageUrl,
        charImgUrl,
        corretRatio,
        moodRatio,
        question,
    )

    return (correctedText, translatedText, saved_imgurl)

    # --- 이미지 저장 부분 임시 코드 --- #
    # imageUrl = f'http://yourserver.com/{filename}'
    # root = "./Backend/provider/diary/tmp_s3/"
    # imageUrl = root + image.filename
    # image.save(imageUrl)
    # --- #
