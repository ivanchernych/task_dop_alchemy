import datetime

from flask import Flask, render_template, redirect
from data import db_session
from users import User
from jobs import Jobs
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.login_form import LoginForm
from forms.job_form import Addjob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def create_spisok():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    jobs = []
    for job in db_sess.query(Jobs).all():
        if job.is_finished:
            finish = 'is finished'
        else:
            finish = 'is not finished'
        jobs.append([job.id, job.job, job.team_leader, job.work_size, job.collaborators, finish])
    return jobs


@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.db")
    jb = create_spisok()
    return render_template('base.html', list=jb)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_form.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_form.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_session.global_init("db/mars_explorer.db")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    form = Addjob()
    if form.validate_on_submit():
        db_session.global_init("db/mars_explorer.db")
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
            start_date=datetime.datetime.now()
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob_form.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=8080,  host='127.0.0.1')
