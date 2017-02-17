from flask import Flask, redirect, request, render_template
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/redirect-test')
def redirectionTest():
    return redirect("http://cs.mcgill.ca/~agaba/")

@app.route('/cow')
def cow():
    return 'Moo!'

@app.route('/centeredText/<userText>')
def templateTest(userText):
    return render_template('test.html', centeredText = userText)

@app.route('/<key>')
def keyTest(key):
    value = r.get(key)
    if (value is None):
        return "GET('" + key + "') --> None"
    else:
        return "GET('" + key + "') --> " + value

if __name__ == '__main__':
   app.run()

