from sqlalchemy import create_engine, and_, desc
from sqlalchemy.orm import sessionmaker
from model.model import PARENTDIARY, PROFILE, CHILDDIARY
from model import databaseConfig, model
from sqlalchemy.sql import extract
from sqlalchemy.orm import scoped_session, sessionmaker

from io import BytesIO
import boto3, os, uuid
from model.s3Config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from model.s3Config import AWS_S3_BUCKET_NAME, AWS_S3_BUCKET_REGION
from werkzeug.utils import secure_filename

import hashlib


engine = None
Session = None
session = None
s3 = None


def init_db():
    global engine
    global Session
    global session
    global s3

    if not engine:
        # mysql database 연결 #
        engine = create_engine(
            databaseConfig.getURI(), pool_size=20, pool_recycle=500, max_overflow=20
        )
        model.init_db(engine)

        # mysql database와 데이터를 주고받을 통신 연결 #
        session = scoped_session(sessionmaker(engine))
        # try:
        #     # this is where the "work" happens!
        #     yield session
        #     # always commit changes!
        #     session.commit()
        # except:
        #     # if any kind of exception occurs, rollback transaction
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()
        print("----- session commit complete -----")

    if not s3:
        s3 = boto3.client(
            service_name="s3",
            region_name=AWS_S3_BUCKET_REGION,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        print("----- s3 bucket connected! -----")


# -- Get(DB에서 값을 불러오는) 함수 --#


# 비밀번호 불러오기
# 로그인 로직에서 사용
def get_pw(id):
    password = session.query(PROFILE.Password).filter(PROFILE.ID == id).first()
    return password


# 개인 고유번호 불러오기
# 로그인 후 로직에서 사용
def get_pid(id):
    pid = session.query(PROFILE.id_profile).filter(PROFILE.ID == id).first()
    return pid


# 사용자 정보 불러오기
# 설정 화면에서 제공
def get_profile(pid):
    profile = session.query(PROFILE).filter(PROFILE.id_profile == pid).first()
    return profile


# 특정 일자 부모 일기 가져오기
# 홈 화면, 소통하기 화면, 통계 일일 리포트에서 제공
def get_parent_diary(pid, date):
    # select_date = date.date()
    parDiary = (
        session.query(PARENTDIARY)
        .filter(and_(PARENTDIARY.id_profile == pid, PARENTDIARY.pd_date == date))
        .first()
    )
    return parDiary


# 특정 일자 아이 일기 가져오기
# 홈 화면, 소통하기 화면, 통계 일일 리포트에서 제공
def get_child_diary(pid, date):
    #    select_date = date.date()
    chiDiary = (
        session.query(CHILDDIARY)
        .filter(and_(CHILDDIARY.id_profile == pid, CHILDDIARY.cd_date == date))
        .first()
    )
    return chiDiary


# 한달 기준 일기 작성된 일자 불러오기
# 홈 화면에서 제공
def get_date(pid, date):
    month = date.month
    date_list = (
        session.query(PARENTDIARY.pd_date)
        .filter(
            and_(
                PARENTDIARY.id_profile == pid,
                extract("month", PARENTDIARY.pd_date) == month,
            )
        )
        .all()
    )
    if date_list is None:
        date_list = []
    return date_list


# 사용자 정보 불러오기
# 설정 화면에서 제공
def get_profile(pid):
    user_profile = session.query(PROFILE).filter(PROFILE.id_profile == pid).first()
    return user_profile


# 최근 7개 부모 일기 통계 불러오기
# 통계 최근 7개 리포트에서 제공
def get_recent7_parent_stats(pid):
    lang_ratio_list = (
        session.query(PARENTDIARY.pd_langRatio)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(7)
        .all()
    )
    correct_ratio_list = (
        session.query(PARENTDIARY.pd_correctRatio)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(7)
        .all()
    )
    dateList = (
        session.query(PARENTDIARY.pd_date)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(7)
        .all()
    )

    return lang_ratio_list, correct_ratio_list, dateList


# 최근 7개 아이 일기 통계 불러오기
# 통계 최근 7개 리포트에서 제공
def get_recent7_child_stats(pid):
    correct_ratio_list = (
        session.query(CHILDDIARY.cd_correctRatio)
        .order_by(desc(CHILDDIARY.id_cd))
        .filter(CHILDDIARY.id_profile == pid)
        .limit(7)
        .all()
    )
    mood_list = (
        session.query(CHILDDIARY.cd_mood)
        .order_by(desc(CHILDDIARY.id_cd))
        .filter(CHILDDIARY.id_profile == pid)
        .limit(7)
        .all()
    )
    dateList = (
        session.query(CHILDDIARY.cd_date)
        .order_by(desc(CHILDDIARY.id_cd))
        .filter(CHILDDIARY.id_profile == pid)
        .limit(7)
        .all()
    )

    return correct_ratio_list, mood_list, dateList


# 최근 30개 부모 일기 통계 불러오기
# 통계 최근 30개 리포트에서 제공
def recent30_parent_stats(pid):
    lang_ratio_list = (
        session.query(PARENTDIARY.pd_langRatio)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(30)
        .all()
    )
    correct_ratio_list = (
        session.query(PARENTDIARY.pd_correctRatio)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(30)
        .all()
    )
    dateList = (
        session.query(PARENTDIARY.pd_date)
        .order_by(desc(PARENTDIARY.id_pd))
        .filter(PARENTDIARY.id_profile == pid)
        .limit(30)
        .all()
    )
    return lang_ratio_list, correct_ratio_list, dateList


# 최근 30개 아이 일기 통계 불러오기
# 통계 최근 30개 리포트에서 제공
def recent30_child_stats(pid):
    correct_ratio_list = (
        session.query(CHILDDIARY.cd_correctRatio)
        .order_by(desc(CHILDDIARY.id_cd))
        .filter(CHILDDIARY.id_profile == pid)
        .limit(30)
        .all()
    )
    dateList = (
        session.query(CHILDDIARY.cd_date)
        .order_by(desc(CHILDDIARY.id_cd))
        .filter(CHILDDIARY.id_profile == pid)
        .limit(30)
        .all()
    )
    return correct_ratio_list, dateList


# S3에서 이미지 불러오는 함수
# 미리보기 화면, 소통하기 화면에서 사용
def get_image_s3(file_name):
    location = s3.get_bucket_location(Bucket=AWS_S3_BUCKET_NAME)["LocationConstraint"]
    print("-- s3 img url call completed --")
    return f"https://{AWS_S3_BUCKET_NAME}.s3.{location}.amazonaws.com/{file_name}"


# -- Set(DB에 값을 집어넣는) 함수 --#


# 사용자 정보 저장
def set_profile(id, pw, pname, page, pcountry, pgender, pnumber, cname, cage, cgender):
    profile = PROFILE(
        ID=id,
        Password=hashlib.sha256(pw.encode()).hexdigest(),
        pName=pname,
        pAge=page,
        pCountry=pcountry,
        pGender=pgender,
        pNumber=pnumber,
        cName=cname,
        cAge=cage,
        cGender=cgender,
    )
    session.add(profile)
    session.commit()


# 부모 다이어리 저장
def set_parent_diary(
    pid,
    date,
    text,
    corrected_text,
    translated_text,
    image,
    char_image,
    langRatio,
    correct_ratio,
    question,
):
    pDiary = PARENTDIARY(
        id_profile=pid,
        pd_date=date,
        pd_text=text,
        pd_corrected=corrected_text,
        pd_translated=translated_text,
        pd_imageURL=image,
        pd_charURL=char_image,
        pd_correctRatio=correct_ratio,
        pd_langRatio=langRatio,
        pd_question=question,
    )
    session.add(pDiary)
    session.commit()


# 아이 다이어리 저장
def set_child_diary(
    pid,
    date,
    corrected_text,
    translated_text,
    image,
    char_image,
    correct_ratio,
    mood_ratio,
    question,
):
    cDiary = CHILDDIARY(
        id_profile=pid,
        cd_date=date,
        cd_corrected=corrected_text,
        cd_translated=translated_text,
        cd_imageURL=image,
        cd_charURL=char_image,
        cd_correctRatio=correct_ratio,
        cd_mood=mood_ratio,
        cd_question=question,
    )
    session.add(cDiary)
    session.commit()


def set_image_s3(file):
    print("-- s3 upload func --")
    filename = secure_filename(file.filename)
    print("--------filename:", filename)
    unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    print("--------filename:", unique_filename)

    s3.upload_fileobj(file, AWS_S3_BUCKET_NAME, unique_filename)
    print("-- s3 img upload completed --")

    return unique_filename


# root = ".\var\lib\docker\Backend\model\img"
# try:
#     if not os.path.exists(root):
#         os.makedirs(root)
# except OSError:
#     print("Error: Creating directory. " + root)

# filename = secure_filename(file.filename)
# if filename == "jpg":
#     unique_filename = str(uuid.uuid4()) + ".jpg"
# else:
#     unique_filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
# key = os.path.join(root, unique_filename)
# print("=========\n=========\n=========", filename, "\n", unique_filename, "\n", key)
# file.save(key)
# s3.upload_fileobj(file, AWS_S3_BUCKET_NAME, key)
# print("-- s3 img upload completed --")
# return key
