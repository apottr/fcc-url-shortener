from flask import Flask,redirect,make_response
import sqlite3,sys,re
app = Flask(__name__)
db = 'url_shortener.db'

def init_db():
	con = sqlite3.connect(db)
	c = con.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS shortened
			(url TEXT)
	''')

@app.route('/url/<index>')
def url_shortener(index):
	con = sqlite3.connect(db)
	c = con.cursor()
	c.execute('''
		SELECT * FROM shortened WHERE rowid=?
	''',(index,))
	result = c.fetchone()
	con.commit()
	con.close()
	if result == None:
		resp = make_response(str({"error": "This url is not in the database."}))
		resp.headers['Content-Type'] = 'application/json'
		return resp
	else:
		return redirect(str(result[0]))

@app.route('/url/new/<path:url>')
def url_shortener_new(url):
	if re.match(r'https?:\/\/.\/?.*',url):
		con = sqlite3.connect(db)
		c = con.cursor()
		c.execute('''
			INSERT INTO shortened VALUES (?)
		''',(url,))
		rowid = c.lastrowid
		con.commit()
		con.close()
		out = {"original_url": str(url), "short_url": "http://floating-mountain-20274.herokuapp.com/url/{}".format(rowid)}
		resp = make_response(str(out))
		resp.headers['Content-Type'] = 'application/json'
		return resp
	else:
		resp = make_response(str({"error": "Wrong url format, make sure you have a valid protocol and real site."}))
		resp.headers['Content-Type'] = 'application/json'
		return resp

if __name__ == "__main__":
	init_db()
	app.run(host="0.0.0.0",port=int(sys.argv[1]))
