from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/chatApp')
def chatApp():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
