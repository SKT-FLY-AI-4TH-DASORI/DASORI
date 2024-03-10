import model.__init__ as db

db.init_db()


def signup(ID, password, pName, pAge, pCountry, pGender, pNumber, cName, cAge, cGender):
    db.set_profile(
        ID, password, pName, pAge, pCountry, pGender, pNumber, cName, cAge, cGender
    )
