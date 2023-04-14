from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")

    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"

    user_2 = User()
    user_2.surname = "Ivan"
    user_2.name = "Chernych"
    user_2.age = 16
    user_2.position = "captain"
    user_2.speciality = "commander in chief"
    user_2.address = "module_5"
    user_2.email = "ivan_chernych@mars.org"
    user_2.hashed_password = "12345436876462562858352324262642"

    user_3 = User()
    user_3.surname = "Oleg"
    user_3.name = "Petrovich"
    user_3.age = 33
    user_3.position = "technician"
    user_3.speciality = "technician"
    user_3.address = "module_3"
    user_3.email = "oleg_petrrr@mars.org"
    user_3.hashed_password = "oleg228"

    user_4 = User()
    user_4.surname = "Misha"
    user_4.name = "Barygov"
    user_4.age = 23
    user_4.position = "member"
    user_4.speciality = "cleaner"
    user_4.address = "module_1"
    user_4.email = "misha_baryga2000@mars.org"
    user_4.hashed_password = "mishanya777"

    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.add(user_2)
    db_sess.add(user_3)
    db_sess.add(user_4)
    db_sess.commit()
    # app.run()


if __name__ == '__main__':
    main()
