from flask import (Flask,
                   redirect,
                   url_for,
                   request,
                   render_template)
import sqlite3
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import bcrypt

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

@App.route('/logged',methods=['GET','POST'])
def logged():
    new_username = request.form['username']
    new_password = request.form['password']
    cursor = connect.execute("SELECT * from USERS_DATA")
    for user in cursor:
        decoded_pw = bcrypt.checkpw(new_password.encode("UTF-8"),user[2])
        if(user[0] == new_username and decoded_pw == True):
            return f'Welcome {user[0]}.'
    else:
        return 'User or password incorrect.'
    
    # return render_template('home.html') 


@App.route('/register')
def register():
    return render_template('register.html')

@App.route('/account-created',methods=['GET','POST'])
def create_user():
    cursor = connect.cursor()
    new_username = request.form['username']
    new_email = request.form['email']
    new_password = request.form['password']
    hashed_pw = bcrypt.hashpw(new_password.encode("UTF-8"),bcrypt.gensalt())
    cursor.execute("INSERT INTO USERS_DATA(username,email,password)VALUES(?,?,?)", (new_username, new_email, hashed_pw))
    connect.commit()
    
    return redirect('/login')

if __name__ == '__main__':
    App.run(debug=True)
