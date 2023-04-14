from flask import Flask, render_template
from data import db_session
from jobs import Jobs
from users import User
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
@app.route('/test')
def test():
    jb = create_spisok()
    return render_template('base.html', list=jb)


if __name__ == '__main__':
    app.run(port=8080,  host='127.0.0.1')
