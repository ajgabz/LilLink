from flask import Flask, redirect, request, render_template, url_for
from flask_reggie import Reggie
import redis
import validators

app = Flask(__name__)
Reggie(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index(shortening_worked = None, url_key = None):
    if (shortening_worked is None):
        return render_template('index.html')
    else:
        return render_template('shortening_result.html', shortening_worked = shortening_worked, urlkey = url_key)

@app.route('/generateURL/', methods=['POST'])
def generate_url():
    user_input = request.form['url']
    if (not validators.url(user_input)):
        return redirect(url_for('index', shortening_worked = False))
    else:
        url_key = hex(r.incr('siteCounter'))[2:]
        r.set(url_key, user_input)
        return redirect(url_for('index', shortening_worked=True, urlkey = url_key))

@app.route('/<regex("[A-Fa-f0-9]+"):urlkey>')
def redirect_user(urlkey):
    numeric_key = str(int(urlkey, base=16))
    url_value = r.get(numeric_key)
    if (url_value is None):
        return render_template('error_page.html', page_title='Redirection Error',
                               error_message="There is no URL associated with this LilLink URL.")
    else:
        return redirect(url_value)

if __name__ == '__main__':
   app.run(debug=True)
