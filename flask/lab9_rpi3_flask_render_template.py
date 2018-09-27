from flask import Flask, render_template

app =Flask(__name__)

@app.route('/')
def home():
	temperature =25
	humidity = 90
	return render_template('index.html', temperature = temperature, humidity=humidity)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port =80, debug=True)
