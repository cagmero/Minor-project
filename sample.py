from flask import Blueprint, render_template, abort
from db import mysql


sample = Blueprint('sample', __name__,template_folder='templates')

@sample.route('/home')
@sample.route('/')
def home():
    # from app import mysql
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * from user_registered")
    data = cursor.fetchone()
    print(data)
    return render_template('user_details.html',data = data)


