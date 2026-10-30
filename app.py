from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def register():
	return render_template('register.html')
@app.route('/submit', methods=['POST'])
def submit():
	name = request.form['username']
	return render_template('success.html', name=name)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=False)