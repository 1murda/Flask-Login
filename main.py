from flask import (Flask,
                   redirect,
                   session,
                   url_for,
                   request,
                   render_template)
import sqlite3
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import bcrypt

App = Flask(__name__)

App.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
App.config['SECRET_KEY'] = 'as897as89dasd'
db = SQLAlchemy(App)

connect = sqlite3.connect('database.db', check_same_thread=False)

@App.route('/')
def default():
    return redirect('/home')

@App.route('/home')
def home():
    if('username' in session):
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
    return render_template('home.html')


@App.route('/login')
def login(methods=['GET']):
    return render_template('login.html')


@App.route('/register')
def register():
    return render_template('register.html')


@App.route('/logged',methods=['GET','POST'])
def logged():
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_password = request.form['password']
        cursor = connect.execute("SELECT * from USERS_DATA")
        
        for user in cursor:
            decoded_pw = bcrypt.checkpw(new_password.encode("UTF-8"),user[2])
            
            if(user[0] == new_username and decoded_pw == True):
                session['username'] = request.form['username']
                return f'Welcome {user[0]}.'

        return 'User or password incorrect.'
    
    # return render_template('home.html')

@App.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home')) 


@App.route('/account-created',methods=['POST'])
def create_user():

    if request.method == 'POST':
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
