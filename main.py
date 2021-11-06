from flask import Flask,render_template,request
import flask

app = Flask(__name__)

@app.route('/')
def route_home():
    return render_template('index.html')

@app.route('/item')
def route_item():
    return render_template('item.html')

if __name__ == '__main__':
    app.run(debug=True)