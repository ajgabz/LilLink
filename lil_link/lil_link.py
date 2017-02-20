from flask import Flask, redirect, request, render_template, url_for, flash
from flask_reggie import Reggie
import redis
import validators

app = Flask(__name__)
app.secret_key = "super_secret_key"
Reggie(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generateURL/', methods=['POST'])
def generate_url():
    user_input = request.form['url']
    if (not validators.url(user_input)):
        error_message = "\"" + user_input + "\" is an invalid URL."
        flash(error_message, category="error")
        return redirect(url_for('index'))
    else:
        url_key = hex(r.incr('siteCounter'))[2:]
        r.set(url_key, user_input)
        generated_url = url_for('redirect_user', urlkey = url_key, _external = True)
        flash('Shortened URL: ' + generated_url, category="success")
        return redirect(url_for('index'))

@app.route('/<regex("[A-Fa-f0-9]+"):urlkey>')
def redirect_user(urlkey):
    url_value = r.get(urlkey.lower())
    if (url_value is None):
        return render_template('error_page.html', page_title='Redirection Error',
                                error_message="There is no URL associated with this LilLink URL.")
    else:
        return redirect(url_value)

if __name__ == '__main__':
   app.run(debug=True)
