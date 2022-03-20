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


def add(*operands_lst):
    """ Returns a STRING with the sum of the arguments """

    # TODONE: Fill sum with the correct value, based on the
    # args provided.
    try:
        total = sum(map(int, operands_lst))
        body = """
        <h2>Addition Page</h2>
        <body>
        <p>The sum is {total}.</p>
        </body>
        """.format(total=total)
    except(ValueError, TypeError):
        body = 'Cannot calculate the sum. Please provide integers for the operands.'

    return body

# TODONE: Add functions for handling more arithmetic operations.

def subtract(*operands_lst):
    try:
        difference = int(operands_lst[0]) - int(operands_lst[1])
        body = """
        <h2>Subtraction Page</h2>
        <body>
        <p>The difference is {difference}.</p>
        </body>
        """.format(difference=difference)
    except(ValueError, TypeError):
        body = 'Cannot calculate the difference. Please provide integers for the operands.'

    return body


def multiply(*operands_lst):
    try:
        product = int(operands_lst[0]) * int(operands_lst[1])
        body = """
        <h2>Multiplication Page</h2>
        <body>
        <p>The product is {product}.</p>
        </body>
        """.format(product=product)
    except(ValueError, TypeError):
        body = 'Cannot calculate the product. Please provide integers for the operands.'
    return body


def divide(*operands_lst):
    try:
        quotient = int(operands_lst[0])/int(operands_lst[1])
        body = """
        <h2>Division Page</h2>
        <body>
        <p>The product is {quotient}.</p>
        </body>
        """.format(quotient=quotient)
    except(ValueError, TypeError):
        body = 'Cannot calculate the quotient. Please provide integers for the operands.'
    return body


def index_page():
    body = """
    <h2>The WSGI Calculator</h2>
    <body>
    <p>Welcome! With this calculator you can:</p>
    <ul>
    <li>add</li>
    <li>subtract</li>
    <li>multiply</li>
    <li>divide</li>
    </ul>
    <p>Enter the operation and two operands in the uri. Like so: </p>
    <ul>
    <li>{This page}/multiply/3/5   => 15</li>
    <li>{This page}/divide/22/11   => 2</li>
    """
    return body



def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODONE: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
        '': index_page,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    # TODONE: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODONE (bonus): Add error handling for a user attempting
    # to divide by zero.
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        #Not sure if 400 would be the correct status code for this.
        body = """<h1>Bad Request</h1>
        <h2>Cannot Divide by Zero</h2>"""
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODONE: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
