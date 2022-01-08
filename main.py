from flask import (Flask,
                   redirect,
                   url_for,
                   request,
                   render_template)

import sqlite3
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

App = Flask(__name__)

App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
App.config['SECRET KEY'] = 'as897as89dasd'
db = SQLAlchemy(App)

connect = sqlite3.connect('database.db', check_same_thread=False)

@App.route('/')
def home():
    return redirect('/login')

@App.route('/login')
def login():
    return render_template('login.html')

@App.route('/register')
def register():
    return render_template('register.html')

@App.route('/account-created',methods=['GET','POST'])
def create_user():
    cursor = connect.cursor()
    new_username = request.form['username']
    new_email = request.form['email']
    new_password = request.form['password']
    cursor.execute("INSERT INTO USERS_DATA(username,email,password)VALUES(?,?,?)", (new_username, new_email, new_password))
    connect.commit()
    
    return 'Account created succefully'

if __name__ == '__main__':
    App.run(debug=True)
