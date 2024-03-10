import hashlib

users = {
    "admin1": hashlib.sha256("asdfghjhgfd".encode()).hexdigest(),
    "admin2": hashlib.sha256("erthrgeggrf".encode()).hexdigest(),
    "admin3": hashlib.sha256("vhbijdjbdkm".encode()).hexdigest(),
    "admin4": hashlib.sha256("lp,lfpvfebb".encode()).hexdigest(),
    "admin5": hashlib.sha256("koinjiuhhuv".encode()).hexdigest(),
}


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
