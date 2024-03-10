import hashlib

import model.__init__ as db

db.init_db()


class LoginService:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        print(self.username, self.password)
        password_hash = hashlib.sha256(self.password.encode()).hexdigest()
        db_password = db.get_pw(self.username)
        print((db_password.Password), (password_hash))
        if db_password.Password == password_hash:
            pid = db.get_pid(self.username)
            return pid.id_profile

    # def result_code(self):
    #     isSuccess =
    #     code =
    #     message =

    # # Verifying Input
    # if not username or not password:
    #     return False, jsonify({"error": "Bad Request"}), 400
    # # Verifying User
    # if username not in users:
    #     return False, jsonify({"error": "Not Found"}), 404
    # # Verifying Password
    # password_hash = hashlib.sha256(password.encode()).hexdigest()
    # if users[username] == password_hash:
    #     return True, jsonify({"message": "OK"}), 200
    # else:
    #     return False, jsonify({"error": "Forbidden"}), 403
