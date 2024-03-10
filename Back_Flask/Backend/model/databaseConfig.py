import pymysql

# mysql database 연결 정보 #
DB_USERNAME = "admin"
DB_PASSWORD = "ekthflwlffj1234"
DB_HOST = "dasori-rds.citt7lnvfebr.ap-northeast-2.rds.amazonaws.com"
DB_SCHEMA = "dasori_schema"
DB_PORT = "3306"


def getURI():
    pymysql.install_as_MySQLdb()
    print("get_uri")
    return "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(
        DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_SCHEMA
    )
