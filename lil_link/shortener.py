from lil_link import app, r
from flask import redirect, request, render_template, url_for, flash
from lil_link.errors import RedisError, RedirectionError, MalformedURLError
import validators
import redis.exceptions


@app.route('/')
def index():
    """ Renders the main page for the app. """
    return render_template('index.html')

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
            flash({'original_url': user_input, 'shortened_url': url_key})
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
        print "Checkpoint A"
        if (url_value is None):
            raise RedirectionError
        else:
            return redirect(url_value)
    except redis.exceptions.ConnectionError:
        raise RedisError


@app.errorhandler(RedisError)
def service_unavailable(error):
    return render_template('error_page.html', page_title = 'Service Unavailable',
                           error_number = 503, http_error_description = 'Service Unavailable',
                           error_message = error.message), 503

@app.errorhandler(MalformedURLError)
def bad_request(error):
    return render_template('error_page.html', page_title = 'Bad Request',
                           error_number = 400, http_error_description = 'Bad Request',
                           error_message = error.message), 400

@app.errorhandler(RedirectionError)
def redirection_error(error):
    return render_template('error_page.html', page_title = 'Page Not Found',
                           error_number = 404, http_error_description = 'Page Not Found',
                           error_message = error.message), 404
