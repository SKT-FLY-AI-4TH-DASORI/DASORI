from flask import Blueprint, request, jsonify
from provider.auths.login import LoginService
from provider.auths import signup

auths_router = Blueprint("auths", __name__)


@auths_router.route("/logIn", methods=["POST"])
def handle_login():
    username = request.json.get("username")
    password = request.json.get("password")

    Login = LoginService(username, password)
    pid = Login.login()

    return jsonify(
        {
            "pid": pid,
        }
    )


@auths_router.route("/signUp", methods=["POST"])
def handle_signup():
    ID = request.json.get("ID")
    password = request.json.get("password")
    pName = request.json.get("pName")
    pAge = request.json.get("pAge")
    pCountry = request.json.get("pCountry")
    pGender = request.json.get("pGender")
    pNumber = request.json.get("pNumber")
    cName = request.json.get("cName")
    cAge = request.json.get("cAge")
    cGender = request.json.get("cGender")

    signup.signup(
        ID, password, pName, pAge, pCountry, pGender, pNumber, cName, cAge, cGender
    )

    return jsonify({"respone": 200})

    # Login = LoginService(username, password)
    # pid = Login.login()

    # return jsonify(
    #     {
    #         "pid": pid,
    #     }
    # )
