from flask import Flask, redirect, request, render_template
import redis
import validators
import re

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/generateURL/', methods=['POST'])
def generate_url():
    user_input = request.form['url']
    if (not validators.url(user_input)):
        return render_template('error_page.html', page_title = 'Error - Invalid URL',
                               error_message = "A LilLink could not be generated as '" + user_input + "' is an invalid URL.")
    else:
        url_key = hex(r.incr('siteCounter'))[2:]
        r.set(url_key, user_input)
        return render_template('success_page.html', page_title = 'New LilLink Generated',
                               original_url = user_input, url_key = url_key)

@app.route('/<url_key>')
def redirect_user(url_key):
    if (re.match('[0-9A-Fa-f]+', url_key) is None):
        return render_template('error_page.html', page_title = 'Redirection Error',
                               error_message = "There is no URL associated with this LilLink URL.")
    else:
        numeric_key = str(int(url_key, base=16))
        url_value = r.get(numeric_key)
        if (url_value is None):
             return render_template('error_page.html', page_title='Redirection Error',
                                    error_message="There is no URL associated with this LilLink URL.")
        else:
             return redirect(url_value)


if __name__ == '__main__':
   app.run()

