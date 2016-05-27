# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import random
import datetime

from flask import Flask, request, session, escape
from flask import render_template, send_file, make_response, redirect, url_for
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

@app.route('/user', methods=['GET'])
def user():
    return render_template('user.html')
@app.route('/realty', methods=['GET'])
def realty():
    return render_template('realty.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    user_email = request.form.get('new_email', None)
    user_pswd = request.form.get('new_passwd', None)
    user_enter_date = str(datetime.date.today())
    user_type = request.form.get('user_type', '0')
    if user_type == '1':
        print 'yes'
        realty_name = request.form.get('realty_name', None)
        realty_date = request.form.get('realty_date', None)
        realty_url = request.form.get('realty_url', None)
    print 'signUp:', user_email, user_pswd, user_enter_date, user_type
    if user_email and user_pswd:
        conn = mysql.connect()
        cursor = conn.cursor()
        if user_type == '0':
            cursor.callproc('sp_renterSignUp',(user_email, user_pswd, user_enter_date))
        else:
            cursor.callproc('sp_realtySignUp',(user_email, user_pswd, realty_name, realty_date, realty_url, user_enter_date))
        data = cursor.fetchall()
        if len(data) == 0:
            conn.commit()
            conn.close()
            if user_type == '0':
                resp = redirect(url_for('user'))
            else:
                resp = redirect(url_for('realty'))
            resp.set_cookie('user_email', user_email)
            return resp
        return 'Failed'
    return 'Failed'

@app.route('/signIn', methods=['POST'])
def signIn():
    user_email = request.form.get('exist_email', None)
    user_pswd = request.form.get('exist_passwd', None)
    user_type = request.form.get('user_type', '0')
    if user_email and user_pswd:
        conn = mysql.connect()
        cursor = conn.cursor()
        if user_type == '0':
            cursor.execute('select 1 from Renter where renter_email = "' + user_email + '" and renter_pswd = "' + user_pswd + '";')
        else:
            cursor.execute('select 1 from Realty where realty_email = "' + user_email + '" and realty_pswd = "' + user_pswd + '";')
        data = cursor.fetchall()
        conn.close()
        if len(data) == 0:
            return 'Sign in failed'
        else:
            if user_type == '0':
                resp = redirect(url_for('user'))
            else:
                resp = redirect(url_for('realty'))
            resp.set_cookie('user_email', user_email)
            return resp
    return 'Sign in failed'

@app.route('/signOut')
def signOut():
    # remove the username from the session if it's there
    # session.pop('user_email', None)
    resp = redirect(url_for('index'))
    resp.set_cookie('user_email', None)
    return resp

if __name__ == '__main__':
	port = int(os.environ.get("PORT", my_port))
	app.run(host='0.0.0.0', port=port)
