# 기존 데이터베이스 -> 객체 모델 #
# pip install sqlacodegen
# sqlacodegen <mysql uri> > model.py # 변경된 내용을 model.py에 저장

# coding: utf-8
from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

# database table, 클래스간 mapping #
# metaclass 생성
Base = declarative_base()  # Base를 상속받은 클래스들은 모두 테이블과 매칭되는 클래스로 인식됨


def init_db(eng):
    Base.metadata.bind = eng
    print("db_init")


class PROFILE(Base):
    __tablename__ = "PROFILE"

    id_profile = Column(Integer, primary_key=True)
    ID = Column(String(20, "utf8mb3_unicode_ci"), nullable=False, unique=True)
    Password = Column(String(20, "utf8mb3_unicode_ci"), nullable=False)
    pName = Column(String(20, "utf8mb3_unicode_ci"), nullable=False)
    pAge = Column(Integer, nullable=False)
    pCountry = Column(String(10, "utf8mb3_unicode_ci"), nullable=False)
    pGender = Column(CHAR(1, "utf8mb3_unicode_ci"), nullable=False, comment="'M / F'")
    pNumber = Column(String(20, "utf8mb3_unicode_ci"), nullable=False)
    cName = Column(String(20, "utf8mb3_unicode_ci"), nullable=False)
    cAge = Column(Integer, nullable=False)
    cGender = Column(CHAR(1, "utf8mb3_unicode_ci"), nullable=False, comment="'M / F'")


class CHILDDIARY(Base):
    __tablename__ = "CHILD_DIARY"

    id_cd = Column(Integer, primary_key=True)
    cd_date = Column(DateTime, nullable=False)
    cd_corrected = Column(String(200, "utf8mb3_unicode_ci"), nullable=False)
    cd_translated = Column(String(200, "utf8mb3_unicode_ci"), nullable=False)
    cd_imageURL = Column(String(500, "utf8mb3_unicode_ci"), nullable=False)
    cd_charURL = Column(String(500, "utf8mb3_unicode_ci"), nullable=False)
    cd_correctRatio = Column(Integer, nullable=False)
    cd_mood = Column(Integer, nullable=False)
    cd_question = Column(String(150, "utf8mb3_unicode_ci"), nullable=False)
    id_profile = Column(
        ForeignKey("PROFILE.id_profile", ondelete="CASCADE"), index=True
    )

    PROFILE = relationship("PROFILE")


class PARENTDIARY(Base):
    __tablename__ = "PARENT_DIARY"

    id_pd = Column(Integer, primary_key=True)
    pd_date = Column(DateTime, nullable=False)
    pd_text = Column(VARCHAR(200), nullable=False)
    pd_corrected = Column(VARCHAR(200), nullable=False)
    pd_translated = Column(VARCHAR(200), nullable=False)
    pd_imageURL = Column(VARCHAR(500), nullable=False)
    pd_charURL = Column(VARCHAR(500), nullable=False)
    pd_langRatio = Column(Integer, nullable=False)
    pd_correctRatio = Column(Integer, nullable=False)
    pd_question = Column(String(150, "utf8mb3_unicode_ci"), nullable=False)
    id_profile = Column(
        ForeignKey("PROFILE.id_profile", ondelete="CASCADE"), nullable=False, index=True
    )

    PROFILE = relationship("PROFILE")
