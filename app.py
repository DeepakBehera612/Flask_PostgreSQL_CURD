import os
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'Secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:admin@localhost/flask_curd"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class employee_flask_curd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


@app.route('/')
def index():
    get_data = employee_flask_curd.query.all()
    return render_template('index.html', employees=get_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = employee_flask_curd(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash('Data inserted successfully.')
        return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        get_data = employee_flask_curd.query.get(request.form.get('id'))
        get_data.name = request.form['name']
        get_data.email = request.form['email']
        get_data.phone = request.form['phone']
        db.session.commit()
        flash('Data updated successfully.')
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    get_data = employee_flask_curd.query.get(id)
    db.session.delete(get_data)
    db.session.commit()
    flash('Data Delete successfully.')
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
