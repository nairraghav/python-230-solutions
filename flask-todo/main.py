from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from models import Task, User

app = Flask(__name__)


@app.route('/')
def redirect_to_all():
    return redirect(url_for('all_tasks'))


@app.route('/all')
def all_tasks():
    return render_template('all.jinja2', tasks=Task.select())


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task_name = request.form['name-input']
        task = Task(name=task_name)
        task.save()
        return redirect(url_for('all_tasks'))
    else:
        return render_template('create.jinja2')


if __name__ == "__main__":
 port = int(os.environ.get("PORT", 5000))
 app.run(host='0.0.0.0', port=port)