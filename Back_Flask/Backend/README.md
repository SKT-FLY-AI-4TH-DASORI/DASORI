# DASORI
Project Dasori: SKT FLY AI 4기 Ziller DaSori 서비스 프로젝트의 Backend Repository입니다.

Backend: 김다은, 문정현, 이가경


---
## 폴더 구조

app: 어플리케이션 구동 폴더</br>
config: 환경 변수 설정이니까 배포할 때 다시 생각해보기</br>
manage.py: 호스팅 서버 주소, 완료된 app을 불러옴</br>
model: 각 DB 별 ORM 관리 폴더 </br>
provider: API 작성 파일 폴더</br>
router: 각 API 별 blueprint 관리 폴더</br>
</br>
.</br>
├── README.md </br>
├── app </br>
│   └── __init__.py </br>
├── config </br>
│   ├── __init__.py </br>
│   └── flask_config.py</br>
├── manage.py</br>
├── model</br>
│   ├── __init__.py</br>
│   └── member_model.py</br>
│   └── parent_model.py</br>
│   └── child_model.py</br>
├── provider</br>
│   ├── __init__.py</br>
│   ├── common_provider.py</br>
│   ├── auths</br>
│   │   ├── __init__.py</br>
│   │   └── signup.py</br>
│   │   └── login.py</br>
│   │   └── find_account.py</br>
│   ├── diary</br>
│   │   ├── __init__.py</br>
│   │   └── diary_management.py</br>
│   └── stats</br>
│       ├── __init__.py</br>
│       ├── parent_stats.py</br>
│       └── child_stats.py</br>
├── requirements.txt</br>
└── router</br>
    ├── __init__.py</br>
    ├── auths</br>
    │   ├── __init__.py</br>
    │   └── auths_router.py</br>
    ├── diary</br>
    │   ├── __init__.py</br>
    │   └── diary_router.py</br>
    └── stats
        ├── __init__.py</br>
        └── stats_router.py</br>