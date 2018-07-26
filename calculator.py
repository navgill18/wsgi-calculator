import traceback
import re
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

def home(*args):
  page = """
  <head>
      <title>WSGI Calculator</title>
  </head>
  <body>
      <h1>HOW TO PLAY:</h1>
      <h2>There are 4 functions: add, subtract, multiply, divide.</h2>
      <h2>Type the URL above and include the function as well as the operands</h2>
      <h2>Example: http://localhost:8080/add/2/1</h2>
      <h2>The above result will print 3 to the screen</h2>
  """
  return page

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    try:
      sum_nums = str(sum(map(int, args)))
    except (ValueError, TypeError):
      sum_nums = "Incorrect values inputted. Please try again."
    finally:
      return sum_nums

def subtract(*args):
  num_one = None
  num_two = None
  diff = None
  try:
    num_one = int(args[0])
    num_two = int(args[1])
    diff = str(num_one - num_two)
  except (ValueError, TypeError):
    diff = "Incorrect values inputted. Please try again."
  finally:
    return diff

def multiply(*args):
  num_one = None
  num_two = None
  mult = None
  try:
    num_one = int(args[0])
    num_two = int(args[1])
    mult = str(num_one*num_two)
  except (ValueError, TypeError):
    mult = "Incorrect values inputted. Please try again."
  finally:
    return mult

def divide(*args):
  num_one = None
  num_two = None
  div = None
  try:
    num_one = int(args[0])
    num_two = int(args[1])
    div = str(round(num_one/num_two, 2))
  except (ValueError, TypeError):
    div = "Incorrect values inputted. Please try again."
  except ZeroDivisionError:
    div = "Cannot divide by 0."
  finally:
    return div

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    funcs = {
    '': home,
    'add': add,
    'subtract': subtract,
    'multiply': multiply,
    'divide': divide
    }
    new_path = path.strip('/').split('/')
    if path == '':
      args = [1, 2]
    else:
      args = new_path[1:]
    func_name = new_path[0]
    try:
      func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
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
      body = "<h1> Not Found </h1>"
    except Exception:
      status = "500 Internal Server Error"
      body = "<h1>Internal Server Error</h1>"
      print(traceback.format_exc())
    finally:
      headers.append(('Content-length', str(len(str(body)))))
      start_response(status, headers)
      return [str(body).encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
