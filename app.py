# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import random
import datetime

from flask import Flask, request
from flask import render_template, send_file, make_response, redirect
from flask.ext.mysql import MySQL

DEBUG = True
static_dir = 'static/'
img_dir = 'static/img/'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# MySQL configurations
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'houserent'
#app.config['MYSQL_DATABASE_CHARSET'] = 'utf-8'
mysql.init_app(app)

conn = mysql.connect()

my_port = 3100
if len(sys.argv) > 1:
	try:
		my_port = int(sys.argv[3])
	except Exception, e:
		my_port = 3100

@app.teardown_request
def teardown_request(exception):
	pass

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    user_email = request.form.get('new_email', None)
    user_pswd = request.form.get('new_passwd', None)
    user_enter_date = str(datetime.date.today())
    user_type = request.form.get('user_type', None)
    print 'signUp:', user_email, user_pswd, user_enter_date, user_type
    if user_email and user_pswd:
        if user_type == None:
            user_type = 0
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_signUp',(user_email, user_pswd, user_enter_date, user_type))
        data = cursor.fetchall()
        if len(data) is 0:
            conn.commit()
            return 'Ok'
        return 'Failed'
    return 'Failed'


if __name__ == '__main__':
	port = int(os.environ.get("PORT", my_port))
	app.run(host='0.0.0.0', port=port)
