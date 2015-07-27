# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os
import time
import random

from flask import Flask, request
from flask import render_template, send_file, make_response, redirect
DEBUG = True
static_dir = 'static/'
img_dir = 'static/img/'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

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
    return "ok"
	
if __name__ == '__main__':
	port = int(os.environ.get("PORT", my_port))
	app.run(host='0.0.0.0', port=port)
