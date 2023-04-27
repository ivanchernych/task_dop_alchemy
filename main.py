import datetime

from flask import Flask, render_template, redirect, request, abort
from data import db_session
from users import User
from jobs import Jobs
from department import Department
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.login_form import LoginForm
from forms.job_form import Addjob
from forms.add_department import AddDepartment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def create_spisok_jobs():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    jobs = []
    for job in db_sess.query(Jobs).all():
        if job.is_finished:
            finish = 'is finished'
        else:
            finish = 'is not finished'
        jobs.append([job.id, job.job, job.team_leader, job.work_size, job.collaborators, finish, job.creates_user_id])
    return jobs


def create_spisok_department():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()

    departments = []

    for dep in db_sess.query(Department).all():
        departments.append([dep.id, dep.title, dep.chief, dep.members, dep.email, dep.creates_user_id])

    return departments


@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.db")
    jb = create_spisok_jobs()
    return render_template('base.html', list=jb)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/department")


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
            start_date=datetime.datetime.now(),
            creates_user_id=current_user.id
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob_form.html', title='Регистрация', form=form)


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = Addjob()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.creates_user_id == current_user.id) |
                                                         (current_user.id == 1))).first()
        if job:
            form.job.data = job.job
            form.team_leader.data = job.team_leader
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.creates_user_id == current_user.id) |
                                                         (current_user.id == 1))).first()
        if job:
            job.job = form.job.data
            job.team_leader = form.team_leader.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob_form.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == id, ((Jobs.creates_user_id == current_user.id) |
                                                     (current_user.id == 1))).first()
    if job:
        db_sess.delete(job)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/department', methods=['GET', 'POST'])
@login_required
def department():
    db_session.global_init("db/mars_explorer.db")
    lst_dep = create_spisok_department()
    return render_template('department.html', list=lst_dep)


@app.route('/adddepartament', methods=['GET', 'POST'])
def adddepartment():
    print('+')
    form = AddDepartment()
    if form.validate_on_submit():
        db_session.global_init("db/mars_explorer.db")
        db_sess = db_session.create_session()
        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
            creates_user_id=current_user.id
        )
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/department')
    return render_template('adddepartment.html', title='adddepartment', form=form)


@app.route('/edit_department/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = AddDepartment()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id, ((Department.creates_user_id == current_user.id) |
                                                                     (current_user.id == 1))).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Department).filter(Department.id == id, ((Department.creates_user_id == current_user.id) |
                                                                     (current_user.id == 1))).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/department')
        else:
            abort(404)
    return render_template('adddepartment.html',
                           title='Редактирование departmenta',
                           form=form
                           )


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Department).filter(Department.id == id, ((Department.creates_user_id == current_user.id) |
                                                                 (current_user.id == 1))).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/department')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
