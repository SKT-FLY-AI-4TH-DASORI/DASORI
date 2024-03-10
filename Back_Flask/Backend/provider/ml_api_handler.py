import requests
import uuid
import time
import json
from googletrans import Translator
from provider.ml import spell_checker
from provider.ml.get_passport import *
import Levenshtein
from transformers import pipeline
import openai
from PIL import Image
from io import BytesIO
from rembg import remove

from werkzeug.datastructures import FileStorage

import tempfile
import os
import imghdr

ocr_api_url = "https://lzp0tb1l50.apigw.ntruss.com/custom/v1/28447/dda07568dbb5b12b36e7c315803ee0742073fbce3a8892c34797f9cf0092f6c5/general"
ocr_secret_key = "ZnZ3Vk9MT0ZLRmZHQVpwY2NKRVVFdXBvR2ZwVld3Z2M="
OPENAI_API_KEY = "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"

# 1. 아이의 그림일기 image_url을 통해 손글씨 인식 함수
def clova_ocr(image_url):
    request_json = {
        "images": [{"format": "jpg", "name": "demo"}],
        "requestId": str(uuid.uuid4()),
        "version": "V2",
        "timestamp": int(round(time.time() * 1000)),
    }

    payload = {"message": json.dumps(request_json).encode("UTF-8")}
    # files = [("file", open(image_file, "rb"))]
    # files = Image.open(image_file)
    response = requests.get(image_url)
    print("=====response", response)
    print("Response status code:", response.status_code)
    # print("response content", response.content[:100])

    img = Image.open(BytesIO(response.content))
    image_format = img.format.lower()
    print("=====img_original", img)
    img = img.rotate(-90, expand=1)
    print("=====img", img)

    img_io = BytesIO()
    img.save(img_io, image_format)
    # img.save(img_io, image_format)  # 이미지 형식에 맞게 이미지를 저장합니다.
    img_io.seek(0)

    # OCR 작업 코드
    # files = [("file", (image_file.filename, image_file.stream))]
    headers = {"X-OCR-SECRET": ocr_secret_key}
    files = {"file": (f"image.{image_format}", img_io, f"image/{image_format}")}

    response = requests.request(
        "POST", ocr_api_url, headers=headers, data=payload, files=files
    )
    result = response.json()
    # 인식된 손글씨를 하나의 문단으로 합치기
    cd_text = " ".join(item["inferText"] for item in result["images"][0]["fields"])
    # temp_file = None
    # try:
    #     temp_file = tempfile.NamedTemporaryFile(delete=False)
    #     image_file.save(temp_file.name)  # 파일을 디스크에 저장합니다.
    #     temp_file.close()

    #     with Image.open(temp_file.name) as img:

    #         )
    #         pass
    # except IOError:
    #     print("Error: File not accessible")
    # finally:
    #     if temp_file:  # 만약 temp_file 변수가 선언되었다면
    #         os.remove(temp_file.name)

    return cd_text


# cd_ocr_text = clova_ocr(image_file)

# 2. 한베 혼합 부모 일기를 한글로 기계 번역하는 함수
def pd_translator(text):
    translator = Translator()
    # 부모 일기에서 한글 이외의 언어가 사용되었는지 확인
    for i in range(len(text.split(" "))):
        word = text.split(" ")[i]
        detected = translator.detect(word)
        # 한글 이외의 언어가 사용되었다면, gpt를 통한 일기 번역
        if detected.lang != "ko":
            openai.api_key = OPENAI_API_KEY
            # 메시지 설정하기
            messages = [
                {
                    "role": "system",
                    "content": "You are a translate machine.",
                },
                {"role": "assistant", "content": text},
                {
                    "role": "user",
                    "content": "베트남어를 한국어로 번역한 문장을 알려줘.",
                },
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125", messages=messages
            )
            answer = response["choices"][0]["message"]["content"]

            break
        # 한글만 사용되었다면 일기를 그대로 출력
        else:
            answer = text

    return answer

# 3. 부모와 아이 일기 베트남어로 번역하는 함수
def diary_translator(text, origin, target):
    translator = Translator()
    output = translator.translate(text, dest=target, src=origin)
    translated = output.text

    return translated


"""pd_kor_translated = diary_translator(pd_text, 'vi', 'ko')
pd_translated = diary_translator(pd_corrected, 'ko', 'vi')
cd_translated = diary_translator(cd_corrected, 'ko', 'vi')
"""

# 4. 부모 일기의 한국어 번역률을 통해 한국어 능력 계산 함수
def translate_ratio(pd_text):
    count = 0
    translator = Translator()
    # 어절마다 끊어서 한국어인지 다른 언어인지 반복문
    for i in range(len(pd_text.split(" "))):
        word = pd_text.split(" ")[i]
        detected = translator.detect(word)

        if detected.lang != "ko":
            count += 1

    pd_langRatio = int((1 - (count / len(pd_text.split(" ")))) * 100)

    return pd_langRatio


# pd_langRatio = translate_ratio(diary)

# 5. 네이버 맞춤법 검사기를 호출해서 부모와 아이 일기 한국어 교정 함수
def kor_correct(text):
    """
    spell_checker_file_path = "./Backend/provider/ml/spell_checker.py"
    passport_key = get_passport_key()
    if passport_key:
        fix_spell_checker_py_code(spell_checker_file_path, passport_key)
    else:
        print("passportKey를 찾을 수 없습니다.")"""

    hanspell_sent = spell_checker.check(text)
    correct = hanspell_sent.checked

    return correct


"""pd_corrected = kor_correct(pd_kor_translated)
cd_corrected = kor_correct(cd_ocr_text)"""

# 6. 원문과 교정문을 비교해서 한국어 교정률 계산 함수
def correctRatio(text, corrected):
    wrong = Levenshtein.distance(text, corrected)
    correct_ratio = int(wrong / len(text) * 100)

    return correct_ratio


"""pd_correctRatio = correctRatio(pd_kor_translated, pd_corrected)
cd_correctRatio = correctRatio(cd_ocr_text, cd_corrected)"""

# 7. 감성 분석을 통해 아이의 기분을 계산하는 함수
def mood(text):
    print("f_start")
    # 감성 분석 모델 불러오기
    classifier = pipeline("text-classification", model="matthewburke/korean_sentiment")
    print("classf set")
    preds = classifier(text, return_all_scores=True)
    print("predict")
    mood_ratio = int(preds[0][1]["score"] * 100)
    print("mood_ratio")
    #mood_ratio = 50
    return mood_ratio


# cd_mood = mood(cd_corrected)

# 8. gpt를 통해 일기 기반으로 질문 생성하는 함수
def create_question(text):
    openai.api_key = OPENAI_API_KEY
    # 메시지 설정하기
    messages = [
        {"role": "system", "content": "이제부터 너는 선생님이야. 일기를 읽고 정말 간단한 질문을 하게 될거야"},
        {"role": "assistant", "content": text},
        {
            "role": "user",
            "content": "이 일기 내용을 기반으로 7세의 아이에게 할 수 있는 간단한 질문 1개만 1문장으로 생성해줘.",
        },
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    answer = response["choices"][0]["message"]["content"]

    return answer


"""cd_question = create_question(cd_corrected)
pd_question = create_question(pd_corrected)"""

# 9. gpt와 dalle3를 통해 일기 기반 캐릭터 생성하는 함수
def create_image(text):
    openai.api_key = OPENAI_API_KEY
    # 메시지 설정하기(일기에서 키워드 단어 추출)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "assistant", "content": text},
        {"role": "user", "content": "이 내용에서 핵심 단어 한개만 뽑아줘."},
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    answer = response["choices"][0]["message"]["content"]
    # 키워드 단어를 통해 캐릭터 생성
    img_response = openai.Image.create(
        model="dall-e-3",
        prompt=f"{answer} 캐릭터만 가운데에 등장하게 생성해줘. 배경은 투명하게 해줘",
        n=1,
        size="1024x1024",
    )
    print("hello5")
    image_url = img_response["data"][0]["url"]
    print("1")
    res = requests.get(image_url)
    print("2", image_url)
    img = Image.open(BytesIO(res.content))
    print("3", img)
    # 캐릭터 주변 불필요한 배경 제거
    output = remove(img)
    print("hello6")

    # 이미지 데이터를 BytesIO 객체에 저장
    img_byte_arr = BytesIO()
    output.save(img_byte_arr, format="PNG")
    # img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    # BytesIO 스트림을 사용하여 FileStorage 객체 생성
    file_storage = FileStorage(
        stream=img_byte_arr, filename="output_file.png", content_type="image/png"
    )
    print(type(file_storage))
    return file_storage

    # img_path = './Backend/model/img/'+output_file+'.png'
    # output.save(img_path)

    # return img_path


"""create_image(cd_corrected)
create_image(pd_corrected)"""
