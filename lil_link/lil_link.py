from flask import Flask, redirect, request, render_template, url_for, flash, abort
from flask_reggie import Reggie
from errors import RedisError, RedirectionError, MalformedURLError
import redis
import validators

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config["DEBUG"] = True
Reggie(app)
r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def index():
    """ Renders the main page for the app. """
    return render_template('new_index.html')


def hex_sans_prefix(number):
    """Generates a hexadecimal string from a base-10 number without the standard '0x' prefix."""
    return hex(number)[2:]

@app.route('/generateURL/', methods=['POST'])
def generate_url():
    """Given a potential URL, this method verifies the input and if it's a valid URL,
       generates a hexadecimal key associated with it, and stores the key-value pair
       in the Redis datastore."""
    user_input = request.form['url']
    if (not validators.url(user_input)):
        raise MalformedURLError(user_input)
    else:
        try:
            url_key = hex_sans_prefix(r.incr('siteCounter'))
            r.set(url_key, user_input)
            generated_url = url_for('redirect_user', urlkey = url_key, _external = True)
            flash('Shortened URL: ' + generated_url, category="success")
            return redirect(url_for('index'))
        except:
            raise RedisError

@app.route('/<regex("[A-Fa-f0-9]+"):urlkey>')
def redirect_user(urlkey):
    """ Given a hexadecimal URL key, this method attempts to retrieve the URL value associated
        with it.  No value returned raises a RedirectionError and if the Redis server
        cannot be reached, a RedisError is raised."""
    try:
        url_value = r.get(urlkey.lower())
        if (url_value is None):
            raise RedirectionError
        else:
            return redirect(url_value)
    except:
        raise RedisError


@app.errorhandler(RedisError)
def service_unavailable(error):
    return render_template('new_error_page.html', page_title = 'Service Unavailable',
                           error_number = 503, http_error_description = 'Service Unavailable',
                           error_message = error.message), 503

@app.errorhandler(MalformedURLError)
def bad_request(error):
    return render_template('new_error_page.html', page_title = 'Bad Request',
                           error_number = 400, http_error_description = 'Bad Request',
                           error_message = error.message), 400

@app.errorhandler(RedirectionError)
def redirection_error(error):
    return render_template('new_error_page.html', page_title = 'Page Not Found',
                           error_number = 404, http_error_description = 'Page Not Found',
                           error_message = error.message), 404



if __name__ == '__main__':
   app.run(debug=True)