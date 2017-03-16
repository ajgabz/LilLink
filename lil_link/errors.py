class RedisError(Exception):
    """ A RedisError is associated with an HTTP 503 error."""
    def __init__(self):
        error_message = "The requested action could not proceed due to an error with the Redis server."
        Exception.__init__(self, error_message)

class MalformedURLError(ValueError):
    """ A MalformedURLError is associated with an HTTP 400 error, which is raised
        when a malformed URL is sent to the 'generateURL' method. """

    def __init__(self, malformed_url):
       error_message = "The given URL \"%s,\" is a malformed URL and as such, " \
                        "a LilLink URL could not be generated." % malformed_url
       ValueError.__init__(self, error_message)

class RedirectionError(KeyError):
    """ A RedirectionError is associated with an HTTP 404 error, which is raised
        when a LilLink key, not associated with any URL, is sent to the server. """

    def __init__(self):
        error_message = "There is no URL associated with this LilLink URL."
        KeyError.__init__(self, error_message)