from flask import Blueprint, request, jsonify
from datetime import datetime
from provider.diary.diary_management import (
    DiaryService,
    writing_parent_diary,
    choosing_parent_diary,
    writing_child_diary,
    choosing_child_diary,
)

diary_router = Blueprint("/home", __name__)


# 홈 화면
@diary_router.route("/home", methods=["GET"])
def DiaryService_displaying_home():
    pid = request.args.get("pid")
    date = request.args.get("date")
    print("==============", pid, date)
    date = datetime.strptime(date, "%Y-%m-%d")

    Diary = DiaryService(date, pid)
    completeList = Diary.get_complete_list()
    parentDto = Diary.get_parent_diary_preview()
    childDto = Diary.get_child_diary_preview()

    return jsonify(
        {
            "completeList": completeList,
            "get_parent_diary_preview": parentDto,
            "get_child_diary_preview": childDto,
        }
    )


# 선택 날짜 클릭시 홈 화면
@diary_router.route("/home/selectedDate", methods=["GET"])
def DiaryService_displaying_home_selected():
    pid = request.args.get("pid")
    date = request.args.get("date")
    date = datetime.strptime(date, "%Y-%m-%d")

    Diary = DiaryService(date, pid)
    parentDto = Diary.get_parent_diary_preview()
    childDto = Diary.get_child_diary_preview()

    return jsonify(
        {
            "get_parent_diary_preview": parentDto,
            "get_child_diary_preview": childDto,
        }
    )


# 부모 일기 작성 화면
@diary_router.route("/home/parent", methods=["POST"])
def handle_writing_parent_diary():
    # Extracting pId, text and image from request
    pid = request.form.get("pid")
    text = request.form.get("text")
    image = request.files["image"]
    date = request.form.get("date")
    print("=============pid", pid)
    print("=============text", text)
    print("=============image", image)
    print("=============date", date)
    date = datetime.strptime(date, "%Y-%m-%d")

    # Calling function "writing_parent_diary"
    correctedText, translatedText, imageUrl, text = writing_parent_diary(
        pid, date, text, image
    )

    return jsonify(
        {
            "correctedText": correctedText,
            "translatedText": translatedText,
            "imageUrl": imageUrl,
            "text": text,
        }
    )


# 부모 일기 작성 결과 화면
# @diary_router.route("/home/parent/result", methods=["GET"])
# def handle_writing_parent_diary_result():
#     # Extracting pId, text and image from request
#     pid = request.args.get("pid")
#     date = request.args.get("date")
#     date = datetime.strptime(date, "%Y-%m-%d")

#     # Calling function "writing_parent_diary_result"
#     parent_diary = choosing_parent_diary(date, pid)
#     correctedText = parent_diary["correctedText"]
#     translatedText = parent_diary["translatedText"]
#     imageUrl = parent_diary["imageUrl"]
#     text = parent_diary["text"]

#     return jsonify(
#         {
#             "correctedText": correctedText,
#             "translatedText": translatedText,
#             "imageUrl": imageUrl,
#             "text": text,
#         }
#     )


# 아이 일기 작성 화면
@diary_router.route("/home/child", methods=["POST"])
def handle_writing_child_diary():
    # Extracting pId, text and image from request
    pid = request.form.get("pid")
    image = request.files["image"]
    date = request.form.get("date")
    date = datetime.strptime(date, "%Y-%m-%d")

    # Calling function "writing_parent_diary"
    correctedText, translatedText, imageUrl = writing_child_diary(pid, date, image)
    return jsonify(
        {
            "correctedText": correctedText,
            "translatedText": translatedText,
            "imageUrl": imageUrl,
        }
    )


# 아이 일기 작성 결과 화면
# @diary_router.route("/home/child/result", methods=["GET"])
# def handle_writing_child_diary_result():
#     pid = request.args.get("pid")
#     date = request.args.get("date")
#     date = datetime.strptime(date, "%Y-%m-%d")

#     # Calling function "writing_parent_diary_result"
#     child_diary = choosing_child_diary(date, pid)
#     correctedText = child_diary["correctedText"]
#     translatedText = child_diary["translatedText"]
#     imageUrl = child_diary["imageUrl"]

#     return jsonify(
#         {
#             "correctedText": correctedText,
#             "translatedText": translatedText,
#             "imageUrl": imageUrl,
#         }
#     )


# 소통하기 화면
@diary_router.route(f"/home/conversation", methods=["GET"])
def handle_conversation():
    pid = request.args.get("pid")
    date = request.args.get("date")
    print("date", type(date))
    date = datetime.strptime(date, "%Y-%m-%d")

    parent_diary = choosing_parent_diary(date, pid)
    child_diary = choosing_child_diary(date, pid)

    return jsonify({"parent_diary": parent_diary, "child_diary": child_diary})
