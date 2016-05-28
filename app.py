# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import random
import datetime
import json

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

@app.route('/signOut', methods=['GET'])
def signOut():
    # remove the username from the session if it's there
    # session.pop('user_email', None)
    resp = redirect(url_for('index'))
    resp.set_cookie('user_email', '', expires=0)
    return resp


@app.route('/addHouse', methods=['POST'])
def addHouse():
    user_email = request.cookies.get('user_email', None)
    if user_email == None:
        return redirect(url_for('index'))
    city = request.form.get('city', None)
    street = request.form.get('street', None)
    rent = request.form.get('rent', None)
    bedroom = request.form.get('bedroom', None)
    bathroom = request.form.get('bathroom', None)
    house_floor = request.form.get('house_floor', None)
    house_size = request.form.get('house_size', None)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_addHouse',(user_email, city, street, 1, rent, bedroom, bathroom, house_floor, house_size))
    data = cursor.fetchall()
    if len(data) == 0:
        conn.commit()
        conn.close()
        #resp = redirect(url_for('index'))
        return 'OK'
    else:
        return 'Failed'

def parseNum(num):
    if num != '#':
        lx = len(num)
        n = num
        op = ' = '
        if num[lx - 1] == '+' :
            n = num[:(lx - 1)]
            op = ' >= '
        return  op, n
    else:
        return '', ''

@app.route('/search', methods=['POST'])
def search():
    # user_email = request.cookies.get('user_email', None)
    # if user_email == None:
    #     return redirect(url_for('index'))
    city = request.form.get('city', '')
    min_rent = str(request.form.get('min_rent', -1))
    max_rent = str(request.form.get('max_rent', 100000))
    if min_rent == '':
        min_rent = '-1'
    if max_rent == '':
        max_rent = '100000'
    print "*", min_rent, "*", max_rent, "*"
    bedroom = request.form.get('bedroom', '')
    bathroom = request.form.get('bathroom', '')
    qstr  = 'select H.*, R.realty_name, R.website, E.env_nearbymarket, E.env_nearbyschool, E.env_safety'
    qstr += ' from House as H, Realty as R, Environment as E where rent >= ' + min_rent + ' and rent <= ' + max_rent
    if city != '':
        qstr += ' and H.env_city = "' + city + '"'
    op, n = parseNum(bedroom)
    if op != '':
        qstr += ' and bedroom' + op + n
    op, n = parseNum(bathroom)
    if op != '':
        qstr += ' and bathroom' + op + n
    qstr += ' and R.realty_email = H.realty_email and H.env_city = E.env_city and H.env_street = H.env_street;'
    qstr += ' and H.availability = 1'
    print qstr
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(qstr)
    res = cursor.fetchall()
    conn.close()
    print res
    columns = [desc[0] for desc in cursor.description]
    print columns
    rows = [dict(zip(columns, r)) for r in res]
    # houseids = tuple([r['houseid'] for r in rows])
    # qstr = 'select houseid from Save where houseid in ' + str(houseids) + ' and renter_email = ' + user_email
    # cursor.execute(qstr)
    # saved = cursor.fetchall()
    # saved = [r for r in saved]
    # print saved
    # for i in range(len(rows)):
    #     rows[i]['saved'] = False
    # for h in saved:
    ret = json.dumps(rows)
    print ret
    return ret

@app.route('/save', methods=['POST'])
def save():
    user_email = request.cookies.get('user_email', None)
    if user_email == None:
        return 'signin'#redirect(url_for('index'))
    houseid = request.form.get('house_id', None)
    if houseid == None:
        return 'nohouse'
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_save',(user_email, houseid))
        data = cursor.fetchall()
        print data
        if len(data) == 0:
            conn.commit()
            conn.close()
            return 'success'
        else:
            conn.close()
            return 'already'
    except Exception, e:
        conn.close()
        return 'invalid user'

@app.route('/unsave', methods=['POST'])
def unsave():
    user_email = request.cookies.get('user_email', None)
    if user_email == None:
        return 'signin'#redirect(url_for('index'))
    houseid = request.form.get('house_id', None)
    if houseid == None:
        return 'nohouse'
    conn = mysql.connect()
    cursor = conn.cursor()
    qstr = 'delete from Save where renter_email = "' + user_email + '" and houseid = ' + houseid ;
    #cursor.callproc('sp_unsave',(user_email, houseid))
    cursor.execute(qstr)
    data = cursor.fetchall()
    if len(data) == 0:
        conn.commit()
        conn.close()
        return 'success'
    else:
        return 'failed'

@app.route('/list', methods=['POST'])
def listRealty():
    user_email = request.cookies.get('user_email', None)
    if user_email == None:
        return 'signin'#redirect(url_for('index'))
    qstr = 'select * from Realty where realty_email = "' + user_email +'"'
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(qstr)
    res = cursor.fetchall()
    conn.close()
    print res
    columns = [desc[0] for desc in cursor.description]
    print columns
    rows = [dict(zip(columns, r)) for r in res]
    return json.dumps(rows)

@app.route('/favorite', methods=['GET'])
def favorite():
    return render_template('favorite.html')

@app.route('/listfavorite', methods=['GET'])
def listfavorite():
    user_email = request.cookies.get('user_email', None)
    if user_email == None:
        return 'signin'#redirect(url_for('index'))
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_favorite', (user_email,))
    res = cursor.fetchall()
    conn.close()
    columns = [desc[0] for desc in cursor.description]
    print columns
    rows = [dict(zip(columns, r)) for r in res]
    return json.dumps(rows)

#@app.route('/change')

if __name__ == '__main__':
	port = int(os.environ.get("PORT", my_port))
	app.run(host='0.0.0.0', port=port)
