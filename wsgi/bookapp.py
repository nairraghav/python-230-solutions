import re

from bookdb import BookDB

DB = BookDB()


def book(book_id):
    book_info = DB.title_info(book_id)
    if book_info:
        body = [f"<h1>{book_info['title']}</h1>",
                "<ul>",
                f"<li>{book_info['isbn']}</li>",
                f"<li>{book_info['publisher']}</li>",
                f"<li>{book_info['author']}</li>",
                "</ul>"]
        return "\n".join(body)
    raise NameError


def books():
    title_rows = DB.titles()
    body = ["<h1>Book List</h1>", "<ul>"]
    for row in title_rows:
        body.append(f"<li><a href=\"book/{row['id']}\">{row['title']}</a></li>")
    body.append("</ul>")
    return "\n".join(body)


def resolve_path(path):
    functions = {
        '': books,
        'book': book
    }

    path = path.strip('/').split('/')
    try:
        function = functions[path[0]]
        arguments = path[1:]
        return function, arguments
    except IndexError:
        raise NameError


def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
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
