from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask_assg1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Data(db.Model):
    name = db.Column(db.String(100))
    state = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    room = db.Column(db.Integer)
    telnum = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(100))
    keywords = db.Column(db.String(100))

    def __init__(self, name, state, salary, grade, room, telnum, picture, keywords):
        self.name = name
        self.state = state
        self.salary = salary
        self.grade = grade
        self.room = room
        self.telnum = telnum
        self.picture = picture
        self.keywords = keywords


# This is the index route where we are going to
# query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees=all_data)


# this route is for inserting data to mysql database via html forms
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        telnum = request.form['telnum']
        picture = request.form['picture']
        keywords = request.form['keywords']

        my_data = Data(name, state, salary, grade, room, telnum, picture, keywords)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('telnum'))

        my_data.name = request.form['name']
        my_data.state = request.form['state']
        my_data.salary = request.form['salary']
        my_data.grade = request.form['grade']
        my_data.grade = request.form['room']
        my_data.telnum = request.form['telnum']
        my_data.picture = request.form['picture']
        my_data.keywords = request.form['keywords']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/telnum/', methods=['GET', 'POST'])
def delete(telnum):
    my_data = Data.query.get(telnum)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
