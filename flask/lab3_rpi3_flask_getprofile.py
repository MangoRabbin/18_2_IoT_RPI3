from flask import Flask

app = Flask(__name__)

URL_CASE1="/iot/<cat>"
URL_CASE2="/iot/<cat>/<mode>"

@app.route(URL_CASE1)
def home():
	return	render_template('indexEx.html') 

@app.route(URL_CASE2)
def get_profile2(cat, mode):
	return 'profile: ' +cat + ' ' + mode

if __name__ == '__main__':
	app.run(host= '0.0.0.0')
