from flask import Flask, make_response, render_template, session, redirect, url_for, flash
from flask import request
import sqlite3
from jinja2 import Template
import json
import requests

app = Flask(__name__)

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'GET':
		print('not ok')
		return render_template('home.html')
	else:
		print('ok')
		base_url = "https://newsapi.org/v2/everything?apiKey=b00da8907fa0441d88891784159e88c3&"
		keyword = request.form['keyword']
		try:
			qkeyword = request.form['qkeyword']
			keyword = request.form['keyword']
			lang = request.form['lang']
			sort = request.form['sort']
			size = request.form['size']

			url = base_url + "q=" + keyword +"&qInTitle=" + qkeyword + "&language=" + lang + "&sortBy=" +sort + "&pageSize=" +size
			priny(url)
		except:
			keyword = request.form['keyword']
			lang = request.form['lang']
			sort = request.form['sort']
			size = request.form['size']

			url = base_url + "q=" + keyword + "&language=" + lang + "&sortBy=" +sort + "&pageSize=" + size
			print(url)
	
		res = requests.get(url)
		print(res)
		data = res.content.decode('utf-8')
		data = json.loads(data)
		return render_template('home.html', data=data['articles'])

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		fname = request.form['fname']
		lname = request.form['lname']
		email = request.form['email']
		cnumber = request.form['cnumber']
		pwd = request.form['pwd']
		# insert = fname "," lname, email, cnumber, pwd
		con = sqlite3.connect('news.db')
		cur = con.cursor()
		cur.execute("INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, CONTACT, PASSWORD) VALUES (?, ?, ?, ?, ? )",(fname, lname, email, cnumber, pwd));
		con.commit()
		con.close()
		return redirect(url_for('home'))
	else:
		return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		pwd = request.form['pwd']
		con = sqlite3.connect('news.db')
		cur = con.cursor()
		cur.execute("SELECT EMAIL FROM users WHERE EMAIL = (?)", (email,))
		users = cur.fetchone()
		con.close()
		users = list(users)
		print(users[0])
		if users[0] == email:
			con = sqlite3.connect('news.db')
			cur = con.cursor()
			cur.execute("SELECT PASSWORD from users where EMAIL = (?)", [email])
			password = cur.fetchone()
			password = list(password) 
			if password[0] == pwd:
				session['username'] = request.form['email']
				return redirect(url_for('home'))
			else:
				flash('Incorrect user name or password')
				return redirect(url_for('login'))
			
		else:
			return 'hello'
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == "GET":
		con = sqlite3.connect('news.db')
		cur = con.cursor()
		cur.execute("SELECT keyword from tags where EMAIL = (?)", [session['username']])
		keywords = cur.fetchall()
		#print(keywords[0][0])
		data = []
		try:		
			for key in keywords:
				data.append(key[0])
		except:
			pass
		return render_template('addkey.html', data=data)
	else:
		key = request.form['search_id']
		print(key)
		con = sqlite3.connect('news.db')
		cur = con.cursor()
		cur.execute("INSERT INTO tags (EMAIL, keyword) VALUES (?, ? )",(session['username'], key));
		con.commit()
		con.close()
		return redirect(url_for('add'))

@app.route('/delete', methods=['POST'])
def delete():
	key = request.form['search_id']
	print(key)
	con = sqlite3.connect('news.db')
	cur = con.cursor()
	cur.execute("DELETE FROM tags WHERE EMAIL = ? AND keyword = ?",(session['username'], key));
	con.commit()
	con.close()
	return redirect(url_for('add'))

@app.route('/feed')
def feed():
	con = sqlite3.connect('news.db')
	cur = con.cursor()
	cur.execute("SELECT keyword from tags where EMAIL = (?)", [session['username']])
	keywords = cur.fetchall()
	data = []
	for key in keywords:
		data.append(key[0])

	articles = []

	for d in data:
		res = requests.get('https://newsapi.org/v2/everything?q='+d+'&sortBy=popularity&apiKey=b00da8907fa0441d88891784159e88c3&pageSize=5')
		result = res.content.decode('utf-8')
		result = json.loads(result)
		articles.append(result['articles'])

	return render_template('feed.html', data=articles)
if __name__ == '__main__':
	app.secret_key = 'some secret key'
	app.run(debug=True)