from flask import Flask, render_template, request, url_for, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

app = Flask(__name__)
app.config.from_object("punchstarter.settings")
manager = Manager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from punchstarter.models import *

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/projects/create/", methods=['GET', 'POST'])
def create():
    import datetime

    if request.method == 'GET':
        return render_template("create.html")
    if request.method == 'POST':
        start_time = datetime.datetime.now()
        time_end = datetime.datetime.strptime(request.form.get("funding_end_date"), "%Y-%m-%d")
        new_project = Project(
            member_id = 1,
            name = request.form.get("project_name"),
            short_description = request.form.get("short_description"),
            long_description = request.form.get("long_description"),
            goal_amount = request.form.get("funding_goal"),
            time_start = start_time,
            time_end = time_end,
            time_created = start_time,
        )
        db.session.add(new_project)
        db.session.commit()

        return redirect(url_for('create'))


