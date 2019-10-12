"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def info():
    # add more instructions
    return "<h1>How To Use</h1>" \
           "<p>Use one of the following keywords and pass in integers to use this calculator</p>" \
           "<ul>" \
           "<li>add</li>" \
           "<li>subtract</li>"\
           "<li>multiply</li>"\
           "<li>divide</li>" \
           "</ul>" \
           "<p>Pass the inputs for the operation after the keyword. Refer the following examples.</p>" \
           "<p>/add/23/42</p>" \
           "<p>/subtract/23/42</p>" \
           "<p>/multiply/3/5</p>" \
           "<p>/divide/22/11</p>"


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    # returns ValueError if not Int
    args = list(map(int, args))
    total = args[0]
    for arg in args[1:]:
        total += arg

    return str(total)


def subtract(*args):
    """ Returns a STRING with the sum of the arguments """
    # returns ValueError if not Int
    args = list(map(int, args))
    total = args[0]
    for arg in args[1:]:
        total -= arg

    return str(total)


def multiply(*args):
    """ Returns a STRING with the sum of the arguments """
    # returns ValueError if not Int
    args = list(map(int, args))
    total = args[0]
    for arg in args[1:]:
        total *= arg

    return str(total)


def divide(*args):
    """ Returns a STRING with the sum of the arguments """
    # returns ValueError if not Int
    args = list(map(int, args))
    total = args[0]
    for arg in args[1:]:
        total /= arg

    return str(total)


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    functions = {
        '': info,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    path = path.strip('/').split('/')
    try:
        function = functions[path[0]]
        arguments = path[1:]
        return function, arguments
    except IndexError:
        raise NameError
    except KeyError:
        raise NameError


def application(environ, start_response):
    headers = [('Content-Type', 'text/html')]
    path = environ.get('PATH_INFO', None)
    try:
        if not path:
            raise NameError
        function, args = resolve_path(path)
        body = function(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>" \
               "<h2>Cannot Divide By Zero</h2>"
    except ValueError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>" \
               "<h2>Arguments Must Be Integers</h2>"
    except Exception as exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
        print(str(exception))
    finally:
        headers.append(('Content-Length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
